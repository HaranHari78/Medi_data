import json
import httpx
import configparser
from openai.lib.azure import AzureOpenAI
from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam
)
from typing import Optional, Dict, Any, List, Union

def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def format_messages(raw_messages: List[Dict[str, str]]):
    """Convert simple dict messages to proper API types"""
    formatted = []
    for msg in raw_messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "system":
            formatted.append(ChatCompletionSystemMessageParam(
                role=role, content=content))
        elif role == "user":
            formatted.append(ChatCompletionUserMessageParam(
                role=role, content=content))
        elif role == "assistant":
            formatted.append(ChatCompletionAssistantMessageParam(
                role=role, content=content))
        elif role == "tool":
            formatted.append(ChatCompletionToolMessageParam(
                role=role, content=content))
    return formatted

def call_openai_api_with_functions(
    model: str,
    messages: List[Dict[str, str]],
    functions: List[Dict[str, Any]],
    function_call: Optional[Dict[str, str]] = None
) -> Optional[Dict[str, Any]]:
    
    config = load_config()
    formatted_messages = format_messages(messages)

    try:
        with httpx.Client(timeout=30.0, verify=False) as client:
            openai_client = AzureOpenAI(
                api_key=config["azure_openai"]["api_key"],
                api_version=config["azure_openai"]["api_version"],
                azure_endpoint=config["azure_openai"]["endpoint"],
                http_client=client
            )
            
            response = openai_client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                functions=functions,
                function_call=function_call or "auto"
            )
            
            if (response.choices and 
                response.choices[0].message.function_call):
                return json.loads(response.choices[0].message.function_call.arguments)
            return None
            
    except Exception as e:
        print(f"⚠️ API Error: {str(e)[:200]}...")
        return None
