import argparse
import sys
import json
from smart_qa.client import LLMClient
from smart_qa.custom_exceptions import LLMAPIError

def load_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Smart QA Tool (Powered by Google Gen AI SDK)")
    parser.add_argument('action', choices=['summarize', 'ask', 'extract'], help="Action to perform")
    parser.add_argument('--text', type=str, help="Direct text input")
    parser.add_argument('--file', type=str, help="Path to text file")
    parser.add_argument('--question', type=str, help="Question for 'ask' mode")
    parser.add_argument('--save', type=str, help="Path to save output")
    parser.add_argument('--clear-cache', action='store_true', help="Clear local cache")

    args = parser.parse_args()

    try:
        client = LLMClient()
        
        if args.clear_cache:
            client.summarize.cache_clear()
            client.ask.cache_clear()
            print("Cache cleared.")

        # Determine Input
        if args.file:
            input_text = load_file(args.file)
        elif args.text:
            input_text = args.text
        else:
            print("Error: Must provide --text or --file")
            sys.exit(1)

        # Execute Action
        result = ""
        if args.action == 'summarize':
            result = client.summarize(input_text)
        elif args.action == 'ask':
            if not args.question:
                print("Error: --question required for 'ask' mode")
                sys.exit(1)
            result = client.ask(input_text, args.question)
        elif args.action == 'extract':
            data = client.extract_entities(input_text)
            result = json.dumps(data, indent=2)

        # Output
        print("\n--- Result ---")
        print(result)

        if args.save:
            with open(args.save, 'w') as f:
                f.write(result)
            print(f"\nSaved to {args.save}")

    except LLMAPIError as e:
        print(f"Operation failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()