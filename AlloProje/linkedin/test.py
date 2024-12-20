from flask import Flask, render_template_string

app = Flask(__name__)

# HTML içeriği
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kopyalama Butonu</title>
    <script>
        function copyText() {
            var textArea = document.getElementById("text-to-copy");
            textArea.select();
            textArea.setSelectionRange(0, 99999);
            document.execCommand("copy");
            alert("Metin kopyalandı!");
        }
    </script>
</head>
<body>
    <h1>HTML Kopyalama Butonu</h1>
    <textarea id="text-to-copy" rows="4" cols="50">Kopyalanacak bu metni seçip kopyalayabilirsiniz.</textarea>
    <button onclick="copyText()">Metni Kopyala</button>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(debug=True)
