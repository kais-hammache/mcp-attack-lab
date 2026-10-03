from dotenv import load_dotenv

load_dotenv()

import anthropic 


FAKE_FILES={"notes.txt": "Buy milk. Call Alice."}

def read_path(path):
    if path not in FAKE_FILES:
        return "Error: file not found"
    return FAKE_FILES[path]
        

client = anthropic.Anthropic()

user_message= "What does the file notes.txt contain?"
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
    ]

response = client.messages.create(
    model="claude-haiku-4-5-20251001", 
    max_tokens=200, 
    tools=tools,
    messages=[ {"role": "user", "content": user_message} ]
)

print(response)


for block in response.content:
    if block.type == "tool_use":
        tool_id = block.id
        result = read_path(block.input["path"])

final = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    tools= tools,                       
    messages=[
        {"role": "user", "content": user_message},        
        {"role": "assistant", "content": response.content},   
        {
            "role": "user",                       
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result,
                }
            ],
        },
    ],
)

print(final)
