import os
from SearchInDatabase import search_entries, build_index
import ollama
import dotenv
import json
import datetime

dotenv.load_dotenv()

class OllamaInteraction:
    def __init__(self):
        self.idx, self.data, self.mdl = build_index()

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_birthday",
                    "description": "Retrieve birthday information based on provided name and/or date details.",
                }
            }
        ]

        self.messages = []


    def add_to_messages(self, resp, name):
        function_call_result_message = {
            "role": "tool",
            "content": resp,
            'name': name
        }
        self.messages.append(function_call_result_message)

    def send_request(self, message: str, date: str) -> str:
        self.messages.append({'role': 'user', 'content': f"Today is {date}. " + message})

        response = ollama.chat(
            model=os.getenv("MODEL_OLLAMA"),
            messages=self.messages,
            tools=self.tools
        )

        self.messages.append(response['message'])
        # print(response)

        if response['message']['tool_calls']:
            for i, tool_call in enumerate(response['message']['tool_calls']):
                print(tool_call)

                if tool_call['function']['name'] == 'get_birthday':
                    resp = search_entries(message, self.idx, self.data, self.mdl)
                    print(resp)

                    self.add_to_messages(resp, tool_call['function']['name'])


            response = ollama.chat(
                model=os.getenv("MODEL_OLLAMA"),
                messages=self.messages
            )

            self.messages.append(response['message'])

        return response['message']


if __name__ == '__main__':
    ollamaInteraction = OllamaInteraction()
    # answer = ollamaInteraction.send_request('When is Julia Brooks birthday?')
    answer = ollamaInteraction.send_request('Who has a birthday on April 5th?')
    print(answer)
