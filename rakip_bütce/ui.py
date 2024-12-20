from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

def paraphrase_text(text):
    input_text = "paraphrase: " + text
    encoding = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**encoding)
    paraphrased_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return paraphrased_text

original_text = "The quick brown fox jumps over the lazy dog."
paraphrased_text = paraphrase_text(original_text)
print(paraphrased_text)