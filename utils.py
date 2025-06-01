# utils.py

from openai import AzureOpenAI
from openai.types.chat import ChatCompletionUserMessageParam
import configparser
import json

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

async def call_openai_with_function(model, prompt, functions, function_name):
    config = load_config()

    try:
        client = AzureOpenAI(
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"],
            azure_endpoint=config["azure_openai"]["endpoint"],
        )

        messages: list[ChatCompletionUserMessageParam] = [
            {"role": "user", "content": prompt}
        ]

        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call={"name": function_name},
        )

        arguments = response.choices[0].message.function_call.arguments
        return json.loads(arguments)

    except Exception as e:
        print(f"🔴 Azure OpenAI call failed: {e}")
        return None
