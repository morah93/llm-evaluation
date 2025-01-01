from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.llm import (
    query_openai, query_huggingface, query_cohere,
    query_anthropic, query_llama, calculate_accuracy,
    calculate_score
)

# Create an APIRouter instance
router = APIRouter()

# Define a data model for the request
class PromptRequest(BaseModel):
    prompt: str
    ground_truth: Optional[str] = None  # Use Optional instead of |

@router.post("/test-llms/")
async def test_multiple_llms(request: PromptRequest):
    prompt = request.prompt
    ground_truth = request.ground_truth or prompt  # Use prompt as ground truth if none provided

    # Query different LLMs
    responses = {}

    try:
        result = query_openai(prompt, ground_truth)
        final_score = calculate_score(result["accuracy"], result["time"])
        responses["OpenAI"] = {
            "response": result["response"],
            "time": result["time"],
            "accuracy": result["accuracy"],
            "score": final_score
        }
    except Exception as e:
        responses["OpenAI"] = {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0, "score": 0.0}

    try:
        result = query_huggingface(prompt, ground_truth)
        final_score = calculate_score(result["accuracy"], result["time"])
        responses["HuggingFace"] = {
          "response": result["response"],
          "time": result["time"],
          "accuracy": result["accuracy"],
          "score": final_score
        }
    except Exception as e:
        responses["HuggingFace"] = {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0, "score": 0.0}

    try:
        result = query_cohere(prompt, ground_truth)
        final_score = calculate_score(result["accuracy"], result["time"])
        responses["Cohere"] = {
          "response": result["response"],
          "time": result["time"],
          "accuracy": result["accuracy"],
          "score": final_score
        }
    except Exception as e:
        responses["Cohere"] = {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0, "score": 0.0}


    try:
        result = query_anthropic(prompt, ground_truth)
        final_score = calculate_score(result["accuracy"], result["time"])
        responses["Anthropic"] = {
          "response": result["response"],
          "time": result["time"],
          "accuracy": result["accuracy"],
          "score": final_score
        }
    except Exception as e:
        responses["Anthropic"] = {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0, "score": 0.0}


    try:
        result = query_llama(prompt, ground_truth)
        final_score = calculate_score(result["accuracy"], result["time"])
        responses["Llama"] = {
          "response": result["response"],
          "time": result["time"],
          "accuracy": result["accuracy"],
          "score": final_score
        }
    except Exception as e:
        responses["Llama"] = {"response": f"Error: {str(e)}", "time": None, "accuracy": 0.0, "score": 0.0}

    return {
        "prompt": prompt,
        "responses": responses,
        "ground_truth": ground_truth
    }
