# Learning script, step N. Not part of the scanner.
from dotenv import load_dotenv

load_dotenv()

import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    tools=[
        {
            "name": "read_file",
            "description": "This tool read a file.",
            "input_schema": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        }
    ],
    messages=[{"role": "user", "content": "What does the file notes.txt contain?"}],
)

print(response)
