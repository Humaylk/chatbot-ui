def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hi! How can I help you today?"
    elif "how are you" in user_input:
        return "I'm just code, but I'm doing great!"
    elif "bye" in user_input:
        return "Goodbye! Have a nice day!"
    else:
        return "Sorry, I don't understand that yet."

print("Welcome to your chatbot! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print("Bot:", chatbot_response(user_input))
  