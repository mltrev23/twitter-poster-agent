"""Module providing hyperbolic api call functions"""
import os
import time
import logging
import requests
from dotenv import load_dotenv


def make_hyperbolic_llama_inference(messages):
    """A function that calls llama 3.3 70B Instruct via hyperbolic api"""
    load_dotenv()

    hyperbolic_api_key = os.environ.get("HYPERBOLIC_API_KEY")

    url = "https://api.hyperbolic.xyz/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hyperbolic_api_key}",
    }
    data = {
        "messages": messages,
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "max_tokens": 512,
        "temperature": 0.9,
        "top_p": 0.9,
    }

    return __make_safe_hyperbolic_inference(url, headers, data)


def make_hyperbolic_sdxl_inference(prompt):
    """A function that calls flux.1 dev via hyperbolic api"""
    load_dotenv()

    hyperbolic_api_key = os.environ.get("HYPERBOLIC_API_KEY")

    url = "https://api.hyperbolic.xyz/v1/image/generation"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {hyperbolic_api_key}",
    }
    data = {
        "model_name": "FLUX.1-dev",
        "prompt": prompt,
        "steps": 30,
        "cfg_scale": 5,
        "enable_refiner": False,
        "height": 1024,
        "width": 1024,
        "backend": "auto",
    }

    return __make_safe_hyperbolic_inference(url, headers, data)


def __make_safe_hyperbolic_inference(url, headers, data, attempts=5):
    for attempt in range(attempts):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error("HTTP error occurred: %s", http_err)
        except requests.exceptions.ConnectionError as conn_err:
            logging.warning("Connection error occurred: %s", conn_err)
        except requests.exceptions.Timeout as timeout_err:
            logging.warning("Timeout error occurred: %s", timeout_err)
        except requests.exceptions.TooManyRedirects as redirect_err:
            logging.warning("Too many redirects: %s", redirect_err)

        msec = attempt * 100 + 500
        logging.warning("Attempt %d failed. Retrying in %d ms...", attempt + 1, msec)
        time.sleep(msec / 1000)

    return None  # Return None or handle the failure case as needed
