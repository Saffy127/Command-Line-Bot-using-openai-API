import openai
import json
import time
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

def save_history(filename, messages):
    with open(filename, 'w') as f:
        json.dump(messages, f)


def load_history(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def show_help():
    help_text ="""
    Available commands:
    - help: show this help message
    - save [filename]: save conversation history to a file
    - load [filename]: load conversation history from a file 
    - clear: clear conversation history
    - quit(): exit program
    """
    print(help_text)


messages = []
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("Say hello to your new assistant!")

RATE_LIMIT_DELAY = 5
last_request_time = 0

while True:
    message = input("")

    if message.lower() == "quit()":
        break
    elif message.lower().startswith("save "):
        filename = message.split(" ")[1]
        save_history(filename, messages)
        print("Conversation history saved successfully.")
    elif message.lower().startswith("load "):
        filename = message.split(" ")[1]
        messages = load_history(filename)
        print("Conversation history cleared.")
    elif message.lower() == "help":
        show_help()
    else:
        messages.append({"role": "user", "content": message})

        current_time = time.time()
        if current_time - last_request_time < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - (current_time - last_request_time))

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print("\n" + reply + "\n")

        last_request_time = time.time()


