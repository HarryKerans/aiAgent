from html import parser
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from available_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")



parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
for x in range(20):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    for candidate in response.candidates:
        messages.append(candidate.content)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if response.usage_metadata != None:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_results = []
    if getattr(response, "function_calls", None):
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call, verbose=args.verbose)
            if not function_call_result.parts:
                raise Exception(f"Function call {function_call.name} did not return any parts")
            result = function_call_result.parts[0].function_response
            if result is None:
                print(f"Function call {function_call.name} did not return a function response")
            if result.response is None:
                print(f"Function call {function_call.name} did not return a response in the function response")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)
        break

    messages.append(types.Content(role="user", parts=function_results))
    if x >= 19:
        print("Error: Maximum number of iterations (20) reached without a final response from the model.")
        exit(1)
