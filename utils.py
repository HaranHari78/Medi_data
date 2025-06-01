import json
import httpx
import configparser
from openai import AzureOpenAI
from openai.types.chat import (
    ChatCompletionToolParam,
    ChatCompletionNamedToolChoiceParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam
)
from typing import Optional, Dict, Any, List, Union, Literal

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
    return formatted

def convert_functions_to_tools(functions: List[Dict[str, Any]]) -> List[ChatCompletionToolParam]:
    """Convert legacy functions format to tools format"""
    return [
        {
            "type": "function",
            "function": {
                "name": func["name"],
                "description": func.get("description", ""),
                "parameters": func["parameters"]
            }
        }
        for func in functions
    ]

def call_openai_api_with_functions(
    model: str,
    messages: List[Dict[str, str]],
    functions: List[Dict[str, Any]],
    function_call: Optional[Union[Dict[str, str], Literal["auto", "none"]]] = None
) -> Optional[Dict[str, Any]]:
    
    config = load_config()
    formatted_messages = format_messages(messages)
    tools = convert_functions_to_tools(functions)

    try:
        with httpx.Client(timeout=30.0, verify=False) as client:
            openai_client = AzureOpenAI(
                api_key=config["azure_openai"]["api_key"],
                api_version=config["azure_openai"]["api_version"],
                azure_endpoint=config["azure_openai"]["endpoint"],
                http_client=client
            )
            
            # Prepare tool_choice
            tool_choice: Union[Literal["auto", "none"], ChatCompletionNamedToolChoiceParam]
            if isinstance(function_call, dict):
                tool_choice = {
                    "type": "function",
                    "function": {"name": function_call["name"]}
                }
            else:
                tool_choice = function_call if function_call else "auto"
            
            response = openai_client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                tools=tools,
                tool_choice=tool_choice
            )
            
            if (response.choices and 
                response.choices[0].message.tool_calls):
                return json.loads(response.choices[0].message.tool_calls[0].function.arguments)
            return None
            
    except Exception as e:
        print(f"⚠️ API Error: {str(e)}")
        return None
