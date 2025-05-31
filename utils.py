import json
import httpx
import configparser
from openai import AzureOpenAI
from typing import Optional, Dict, Any, List
import multiprocessing
from multiprocessing import Queue

def load_config():
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
    Call Azure OpenAI with function calling.
    Returns parsed JSON arguments from function call.
    """
    config = load_config()
    
    try:
        client = AzureOpenAI(
            api_key=config["azure_openai"]["api_key"],
            api_version=config["azure_openai"]["api_version"],
            azure_endpoint=config["azure_openai"]["endpoint"],
            timeout=30.0  # Request timeout
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
        print(f"⚠️ API Error: {str(e)[:200]}...")  # Truncate long errors
        return None

def extract_with_timeout(func, timeout_sec=30):
    """
    Run a function with timeout using multiprocessing.
    Returns None if timeout occurs.
    """
    def worker(q):
        try:
            q.put(func())
        except Exception as e:
            q.put(None)
    
    q = Queue()
    p = multiprocessing.Process(target=worker, args=(q,))
    p.start()
    p.join(timeout=timeout_sec)
    
    if p.is_alive():
        p.terminate()
        p.join()
        return None
    
    return q.get() if not q.empty() else None
