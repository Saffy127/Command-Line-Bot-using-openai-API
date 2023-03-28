import openai
import json
import time
import os
from cryptography.fernet import Fernet

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data.encode()).decode()

def save_history(filename, messages, key):
    encrypted_messages = [encrypt_data(json.dumps(message), key) for message in messages]
    with open(filename, 'w') as f:
        json.dump(encrypted_messages, f)

def load_history(filename, key):
    with open(filename, 'r') as f:
        encrypted_messages = json.load(f)
    return [json.loads(decrypt_data(message, key)) for message in encrypted_messages]

def show_help():
    help_text ="""
    Available commands:
    - help: show this help message
    - save [filename]: save conversation history to a file (encrypted)
    - load [filename]: load conversation history from a file (decrypted)
    - clear: clear conversation history
    - quit(): exit program
    - generate_key: generate a new encryption key
    """
    print(help_text)

encryption_key = generate_key()

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
        save_history(filename, messages, encryption_key)
        print("Conversation history saved successfully.")
    elif message.lower().startswith("load "):
        filename = message.split(" ")[1]
        messages = load_history(filename, encryption_key)
        print("Conversation history loaded.")
    elif message.lower() == "help":
        show_help()
    elif message.lower() == "generate_key":
        encryption_key = generate_key()
        print(f"New encryption key generated: {encryption_key.decode()}")
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
