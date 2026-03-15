import os
import json
import time
import logging
import functools
from typing import Dict, Any, Callable
from dotenv import load_dotenv
from google import genai

from .custom_exceptions import LLMAPIError

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def retry_with_backoff(retries: int =3, backoff_in_seconds:int = 2):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error = str(e).lower()
                    if "503" in error or "service unavailable" in error:
                        if x == retries:
                            logger.error(f"Max retries reached. Error: {e}")
                            raise LLMAPIError(f"Max retries reached. Last error: {e}")
                        sleep = (backoff_in_seconds ** x)
                        logger.warning(f"API is busy. Retrying in {sleep} seconds...")
                        time.sleep(sleep)
                        x += 1
                    else:
                        logger.error(f"Non-retryable error occurred: {e}")
                        raise LLMAPIError(f"API Error: {e}")
        return wrapper
    return decorator

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'gemini-2.5-flash'
    
    @retry_with_backoff(retries=3, backoff_in_seconds=2)
    def _call_api(self, prompt:str) -> str:
        logger.info("Hitting the Google API...")

        response = self.client.models.generate_content(
            model = self.model_name,
            contents = prompt
        )

        if not response.text:
            raise LLMAPIError("Empty response from LLM API.")
        
        return response.text
    
    @functools.lru_cache(maxsize=128)
    def summarize(self, text: str) -> str:
        logger.info("Summarize called (Checking Cache ....)")
        prompt = f"Please provide a concise summary of the following text: \n\n{text}"
        return self._call_api(prompt)
    
    @functools.lru_cache(maxsize=128)
    def ask(self, context: str, question: str) -> str:
        logger.info("Ask called (Checking Cache ....)")
        prompt = f"Context: {context}\n \nQuestion: {question}\n\nAnswer based ONLY on the context provided:"
        return self._call_api(prompt)
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        logger.info("Extract Entities called")

        prompt = (
            f"Extract the key entities (People, Dates, Locations) from the text provided. "
            f"Return ONLY a VALID JSON object. Do not use any markdown formatting.\n\nText: {text}\n\n"
            f"Text: {text}"
        )

        raw_response = self._call_api(prompt)

        cleaned_response = raw_response.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response. Raw output: {raw_response}")
            raise LLMAPIError(f"Model did not return valid JSON. Error: {e}")

