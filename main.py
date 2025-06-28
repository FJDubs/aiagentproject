import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


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
            verbose_content(client, messages)
    except IndexError:
        generate_content(client, messages)


def generate_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print("Response:")
    print(response.text)

def verbose_content(client, messages):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    print(f'User prompt: {messages[0].parts[0].text}')
    print("Response:")
    print(response.text)
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()
