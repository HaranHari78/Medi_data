import json
import httpx
import configparser
from openai import AzureOpenAI
from typing import Optional, Dict, Any, List

def load_config() -> configparser.ConfigParser:
    """Load API config from config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def call_openai_api_with_functions(
    model: str,
    messages: List[Dict[str, str]],
    functions: List[Dict[str, Any]],
    function_call: Optional[Dict[str, str]] = None
) -> Optional[Dict[str, Any]]:
    """
    Generic function to call Azure OpenAI with function calling.
    Returns parsed JSON arguments from function call or None.
    """
    config = load_config()

    try:
        # Custom HTTP client for timeouts/retries
        with httpx.Client(timeout=30.0, verify=False) as custom_http_client:
            client = AzureOpenAI(
                api_key=config["azure_openai"]["api_key"],
                api_version=config["azure_openai"]["api_version"],
                azure_endpoint=config["azure_openai"]["endpoint"],
                http_client=custom_http_client
            )
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call=function_call or "auto"
            )
            
            if response.choices and response.choices[0].message.function_call:
                return json.loads(response.choices[0].message.function_call.arguments)
            return None
            
    except Exception as e:
        print(f"⚠️ API Error: {str(e)[:200]}...")
        return None
