# Learning script, step N. Not part of the scanner.
from dotenv import load_dotenv

load_dotenv()

import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    messages=[{"role": "user", "content": "print Hello World!"}],
)

print(response)
