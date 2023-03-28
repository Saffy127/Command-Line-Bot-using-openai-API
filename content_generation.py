import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Authenticate with the OpenAI API
openai.api_key = api_key

# Function to generate content using OpenAI API
def generate_content(prompt, model='text-davinci-002', max_tokens=100):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )

    content = response.choices[0].text.strip()
    return content

# Example usage
if __name__ == "__main__":
    prompt = "Write a short blog post about the benefits of exercise."
    generated_content = generate_content(prompt)
    print(generated_content)
