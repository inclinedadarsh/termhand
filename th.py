#!/usr/bin/env python3

import os
import configparser
import argparse
import google.generativeai as genai
import subprocess


def main():
    prompt = get_prompt()

    api_key = get_api_key()
    if not api_key:
        print(
            "Error: API Key not found. Please make sure it is configured in the configuration file."
        )
        return

    chat = get_chat(api_key)
    message = f'You have to send the exact command for me to directly copy paste in my linux terminal and use it based on the given request. Don\'t even format with backticks of markdown like syntax. Simply return the command in response. Given request is: "{prompt}"'
    response = chat.send_message(message)
    command = response.parts[0].text.rstrip()

    print(f"Generated command: {command}")
    confirm = input("Do you want to execute the command? (Y/n): ").strip().lower()

    if confirm == "y" or confirm == "":
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
    else:
        print("Execution cancelled!")


def get_prompt():
    parser = argparse.ArgumentParser(
        description="Generate terminal command from natural language prompt"
    )
    parser.add_argument("prompt", type=str, help="The natural language prompt")
    args = parser.parse_args()
    return args.prompt


def get_chat(key):
    genai.configure(api_key=key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    chat = model.start_chat()
    return chat


def get_api_key():
    config_file_path = os.path.expanduser("~/.config/termhand/termhand_config.ini")
    if not os.path.exists(config_file_path):
        return None

    config = configparser.ConfigParser()
    config.read(config_file_path)
    if "termhand" in config and "api_key" in config["termhand"]:
        return config["termhand"]["api_key"]
    else:
        return None


if __name__ == "__main__":
    main()
