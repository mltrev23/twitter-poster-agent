import os
import time
import requests
from dotenv import load_dotenv
import logging


def make_hyperbolic_llama_inference(messages):
    load_dotenv()

    hyperbolic_api_key = os.environ.get('HYPERBOLIC_API_KEY')

    url = "https://api.hyperbolic.xyz/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hyperbolic_api_key}"
    }
    data = {
        "messages": messages,
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "max_tokens": 512,
        "temperature": 0.9,
        "top_p": 0.9
    }

    return __make_safe_hyperbolic_inference(url, headers, data)

def make_hyperbolic_sdxl_inference(prompt):
    load_dotenv()

    hyperbolic_api_key = os.environ.get('HYPERBOLIC_API_KEY')

    url = "https://api.hyperbolic.xyz/v1/image/generation"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hyperbolic_api_key}"
    }
    data = {
        "model_name": "FLUX.1-dev",
        "prompt": prompt,
        "steps": 30,
        "cfg_scale": 5,
        "enable_refiner": False,
        "height": 1024,
        "width": 1024,
        "backend": "auto"
    }

    return __make_safe_hyperbolic_inference(url, headers, data)

def __make_safe_hyperbolic_inference(url, headers, data, attempts = 5):
    for attempt in range(attempts):
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.json()
        except:
            msec = attempt * 100 + 500
            logging.debug(f'Attempt {attempt} failed. Retrying in {msec} ms...')
            time.sleep(msec / 1000)