from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model tokenizer (vocabulary)
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')

# Encode some text to type IDs (numbers)
input_ids = tokenizer.encode('Hey, how are you today? what', return_tensors='pt')

# Load pre-trained model (weights)
model = GPT2LMHeadModel.from_pretrained('distilgpt2')

# Generate a sequence of text
output = model.generate(input_ids, max_length=50, num_return_sequences=1)

# Decode the generated text back to a string
text = tokenizer.decode(output[0], skip_special_tokens=True)

print(text)
