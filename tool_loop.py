from dotenv import load_dotenv

load_dotenv()

import anthropic 


FAKE_FILES={"notes.txt": "Buy milk. Call Alice."}

def read_path(path):
    if path not in FAKE_FILES:
        return "Error: file not found"
    return FAKE_FILES[path]
        

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5-20251001", 
    max_tokens=200, 
    tools=[{ 
        "name": "read_file",
        "description": "This tool read a file.", 
        "input_schema": {

                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"],
            },
        }
    ],
    messages=[ {"role": "user", "content": "What does the file secret.txt contain?"} ]
)

print(response)


for block in response.content:
    if block.type == "tool_use":
        result = read_path(block.input["path"])
        print(result)
