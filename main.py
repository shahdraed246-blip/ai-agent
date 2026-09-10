import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from call_function import call_function, available_functions
from prompts import system_prompt

MAX_ITERATIONS = 20


def generate_content(client, messages, verbose):
    response = client.chat.completions.create(
        model="gemini-flash-lite-latest",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    if response.usage is None:
        raise RuntimeError(
            "No usage data returned from the API — the request may have failed"
        )

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose)
        messages.append(result_message)
        if verbose:
            print(f"-> {result_message['content']}")

    return None


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(MAX_ITERATIONS):
        final_response = generate_content(client, messages, args.verbose)
        if final_response is not None:
            print("Final response:")
            print(final_response)
            return

    print("Error: max iterations reached without a final response")
    exit(1)


if __name__ == "__main__":
    main()
