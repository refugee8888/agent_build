import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from functions import call_functions
from prompts import system_prompt
from functions.call_functions import available_functions
from functions.call_functions import call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Key not found.")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)
if response.usage_metadata.prompt_token_count is not None:
    x = response.usage_metadata.prompt_token_count
else:
    raise RuntimeError("Not found.")
if response.usage_metadata.candidates_token_count is not None:
    y = response.usage_metadata.candidates_token_count
else:
    raise RuntimeError("Not found.")
if args.verbose:
    print(
        f"""User prompt: {args.user_prompt}\nPrompt tokens: {x}\nResponse tokens: {y}"""
    )
if response.function_calls is not None:
    f_result_list = []
    for f in response.function_calls:
        function_call_result = call_function(f, args.verbose)
        if not function_call_result.parts:
            raise Exception("Can't be None")
        if not function_call_result.parts[0].function_response:
            raise Exception("Can't be None")
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Can't be None")
        f_result_list.append(function_call_result.parts[0])
        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

print(response.text)


def main():
    print("Hello from agent-proj!")


if __name__ == "__main__":
    main()
