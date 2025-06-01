# utils.py

import configparser
import httpx
import asyncio
import json
from openai import AzureOpenAI

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

async def call_openai_with_function(model, prompt, functions, function_name):
    config = load_config()
    client = AzureOpenAI(
        api_key=config["azure_openai"]["api_key"],
        api_version=config["azure_openai"]["api_version"],
        azure_endpoint=config["azure_openai"]["endpoint"],
        timeout=30.0
    )

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            functions=functions,
            function_call={"name": function_name},
        )
        arguments = response.choices[0].message.function_call.arguments
        return json.loads(arguments)
    except Exception as e:
        print(f"Function call error: {e}")
        return None
