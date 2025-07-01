import os

import ollama
import dotenv

dotenv.load_dotenv()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_birthday",
            "description": "Search for a birthday date in the database",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get the weather for, e.g. San Francisco, CA"
                    },
                    "format": {
                        "type": "string",
                        "description": "The format to return the weather in, e.g. 'celsius' or 'fahrenheit'",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location", "format"]
            }
        }
    }
]


def send_request(message: str) -> str:
    messages = [
        {'role': 'user', 'content': message},
    ]

    response = ollama.chat(
        model=os.getenv("MODEL_OLLAMA"),
        messages=messages,
        tools=tools
    )

    messages.append(response['message'])

    print(response)
    print(type(response))

    return response['message']['tool_calls']


if __name__ == '__main__':
    send_request('What is the weather in Toronto?')