import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompt import system_prompt
from functions.call_function import call_function, available_functions

def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = args[0]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    try:
        if args[1] == '--verbose':
            generate_content(client, messages, True)
    except IndexError:
        generate_content(client, messages)

def generate_content(client, messages, verbose=False):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if verbose:
        print(f'User prompt: {messages[0].parts[0].text}')
    calls = response.function_calls
    function_call_results = []
    if calls:
        for call in calls:
            try:
                result = call_function(call, verbose)
                function_call_results.append(result)
            except Exception as e:
                raise e
    else:
        print("Response:")
        print(response.text)
    if verbose:
        for result in function_call_results:
            print(f"-> {result.parts[0].function_response.response}")
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
