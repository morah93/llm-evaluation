import os
from dotenv import load_dotenv
import requests
import json
import cohere
from llamaapi import LlamaAPI
from transformers import pipeline
from openai import OpenAI
import time
from difflib import SequenceMatcher

# Initialize API clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
llama = LlamaAPI(os.getenv("LLAMA_API_KEY"))

# CALCULATE ACCURACY
def calculate_accuracy(response: str, ground_truth: str):
    similarity = SequenceMatcher(None, response.lower(), ground_truth.lower()).ratio()
    return similarity * 100

load_dotenv()


# SCORING LOGIC
def calculate_score(accuracy: float, speed: float, max_speed: float = 2.0):
    speed_score = max(0, (max_speed - speed) / max_speed * 100)
    final_score = 0.7 * accuracy + 0.3 * speed_score
    return final_score

# OPENAI

def query_openai(prompt: str, ground_truth: str):
    try:
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        elapsed_time = time.time() - start_time
        result = response.choices[0].message.content.strip()
        accuracy = calculate_accuracy(result, ground_truth)
        return {"response": result, "time": elapsed_time, "accuracy": accuracy}
    except Exception as e:
        return {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0}

# HUGGINGFACE

hf_pipeline = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

def query_huggingface(prompt: str, ground_truth: str):
    try:
        start_time = time.time()
        response = hf_pipeline(prompt, max_length=50, num_return_sequences=1)
        elapsed_time = time.time() - start_time
        result = response[0]['generated_text']
        accuracy = calculate_accuracy(result, ground_truth)
        return {"response": result, "time": elapsed_time, "accuracy": accuracy}
    except Exception as e:
        return {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0}

# COHERE

def query_cohere(prompt: str, ground_truth: str):
    try:
        start_time = time.time()
        response = cohere_client.generate(
            model="command-xlarge-nightly",  # Update this to a valid model name
            prompt=prompt,
            max_tokens=150
        )
        elapsed_time = time.time() - start_time
        result = response.generations[0].text.strip()
        accuracy = calculate_accuracy(result, ground_truth)
        return {"response": result, "time": elapsed_time, "accuracy": accuracy}
    except Exception as e:
        return {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0}

# ANTHROPIC

def query_anthropic(prompt: str, ground_truth: str):
    try:
        start_time = time.time()
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": os.getenv('ANTHROPIC_API_KEY'),
            "anthropic-version": "2024-02-29",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "system": "You are a helpful AI assistant."
        }
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        elapsed_time = time.time() - start_time

        # Debug prints
        print("Status Code:", response.status_code)
        print("Response:", response_data)

        if "error" in response_data:
            return {"response": f"API Error: {response_data['error'].get('message', 'Unknown error')}",
                   "time": elapsed_time,
                   "accuracy": 0.0}

        if response.status_code == 200:
            result = response_data.get("content", [{}])[0].get("text", "").strip()
            accuracy = calculate_accuracy(result, ground_truth)
            return {"response": result, "time": elapsed_time, "accuracy": accuracy}
        else:
            return {"response": f"Error: {response.text}", "time": elapsed_time, "accuracy": 0.0}
    except Exception as e:
        return {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0}
    #     return response_data.get("content", [{}])[0].get("text", "").strip()
    # except Exception as e:
    #     return f"Error: {str(e), "time": elapsed_time, "accuracy": 0.0}"

# LLAMA

def query_llama(prompt: str, ground_truth: str):
    try:
        start_time = time.time()
        api_request_json = {
            "model": "llama3.1-70b",
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }
        response = llama.run(api_request_json)
        elapsed_time = time.time() - start_time
        result = json.dumps(response.json(), indent=2)
        accuracy = calculate_accuracy(result, ground_truth)
        return {"response": result, "time": elapsed_time, "accuracy": accuracy}
    except Exception as e:
        return {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0}
