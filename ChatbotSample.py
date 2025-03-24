from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can use "distilgpt2" for a smaller model
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to generate chatbot response
def generate_response(prompt):
    # Encode input prompt to tokens
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generate a response from the model
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id)
    
    # Decode the generated tokens into text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Chatbot loop
def chat():
    print("Chatbot: Hello! I'm here to chat with you. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        response = generate_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat()
