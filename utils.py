# utils.py

import configparser
import json
from openai import AzureOpenAI


def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def call_openai_with_function(model, prompt, functions, function_name):
    config = load_config()

    try:
        client = AzureOpenAI(
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"],
            azure_endpoint=config["azure_openai"]["endpoint"],
        )

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            functions=functions,
            function_call={"name": function_name}
        )

        arguments = response.choices[0].message.function_call.arguments
        return json.loads(arguments)

    except Exception as e:
        print(f"❌ Azure OpenAI call failed: {e}")
        return None
