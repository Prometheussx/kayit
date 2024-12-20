import json
import requests
from flask import Flask, request, jsonify
from openai import OpenAI
import custom_functions
from waitress import serve
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

load_dotenv()

# Create Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI()

# Global variable to store PDF text
pdf_text_cache = ""

# Function to create or load assistant
def create_or_load_assistant():
    assistant_json_path = "assistant.json"
    # Check if assistant.json exists
    if not os.path.exists(assistant_json_path):
        print("assistant.json not found. Creating a new assistant...")
        # Create a new assistant and save its details to assistant.json
        assistant_id = custom_functions.create_assistant(client)
        with open(assistant_json_path, "w") as f:
            json.dump({"assistant_id": assistant_id}, f)
    else:
        # Load the assistant ID from assistant.json
        with open(assistant_json_path, "r") as f:
            data = json.load(f)
            assistant_id = data.get("assistant_id")
            if not assistant_id:
                raise ValueError("Assistant ID is missing in assistant.json")
    return assistant_id

# Create or load assistant
assistant_id = create_or_load_assistant()

def delete_assistant(assistant_id):
    client.beta.assistants.delete(assistant_id=assistant_id)
    print(f"Assistant with ID {assistant_id} has been deleted.")

def download_and_extract_text_from_pdf(pdf_url):
    global pdf_text_cache
    response = requests.get(pdf_url)
    response.raise_for_status()
    pdf_file = BytesIO(response.content)
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    pdf_text_cache = text  # Cache the extracted text
    return text

def text_to_pdf(text, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    # Split text into lines and add them to the PDF
    lines = text.splitlines()
    y = height - 40  # Start position
    line_height = 14
    for line in lines:
        if y < 40:  # New page
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 40
        c.drawString(40, y, line)
        y -= line_height

    c.save()

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    global assistant_id
    data = request.json
    pdf_url = data.get('pdf_url')

    if not pdf_url:
        return jsonify({"error": "Missing pdf_url"}), 400

    try:
        # Define file paths
        txt_path = "main.txt"
        pdf_path = "main.pdf"
        assistant_json_path = "assistant.json"

        # Download and extract text from the PDF
        pdf_text = download_and_extract_text_from_pdf(pdf_url)

        # Save text to a .txt file
        with open(txt_path, "w", encoding='utf-8') as file:
            file.write(pdf_text)

        # Convert the .txt file to a .pdf file
        text_to_pdf(pdf_text, pdf_path)

        # Remove the .txt file after creating the .pdf
        if os.path.exists(txt_path):
            os.remove(txt_path)

        # Delete the existing assistant
        delete_assistant(assistant_id)

        # Remove the assistant.json file if it exists
        if os.path.exists(assistant_json_path):
            os.remove(assistant_json_path)

        # Create a new assistant and update assistant.json
        assistant_id = custom_functions.create_assistant(client)

        return jsonify({"message": "main.pdf created successfully from main.txt, main.txt deleted, assistant.json removed and recreated, and assistant updated with new PDF."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/start', methods=['GET'])
def start_conversation():
    print("Starting a new conversation...")
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")
    return jsonify({"thread_id": thread.id})

@app.route('/chat', methods=['POST'])
def chat():
    global pdf_text_cache  # Use cached PDF text
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')

    if not thread_id:
        print("Error: Missing thread_id")
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")

    # Combine cached PDF text with user input
    combined_input = f"PDF Content: {pdf_text_cache}\n\nUser Message: {user_input}"

    # Add the combined input to the thread
    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=combined_input)

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread_id,
                                          assistant_id=assistant_id)

    # Check if the Run requires action (function call)
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                       run_id=run.id)
        if run_status.status == 'completed':
            break
        elif run_status.status == 'requires_action':
            for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "create_lead":
                    arguments = json.loads(tool_call.function.arguments)
                    name = arguments.get('name', '')
                    phone = arguments.get('phone', '')
                    email = arguments.get('email', '')

                    output = custom_functions.create_lead(name, phone, email)
                    client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id,
                                                                 run_id=run.id,
                                                                 tool_outputs=[{
                                                                     "tool_call_id": tool_call.id,
                                                                     "output": json.dumps(output)
                                                                 }])


    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value

    print(f"Assistant response: {response}")
    return jsonify({"response": response})

if __name__ == '__main__':
    serve(app, host='localhost', port=8080)
