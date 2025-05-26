# app/llm_integrations.py
import asyncio
from typing import Optional, Dict, Any
import httpx # For async HTTP requests if calling real APIs
from .config import settings

# --- Base LLM API Class (Conceptual) ---
class BaseLLMAPI:
    def __init__(self, api_key: Optional[str], base_url: str, model_name: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.active_requests = 0

    async def generate_text(self, prompt: str, max_tokens: int, temperature: float = 0.7) -> str:
        raise NotImplementedError("Subclasses must implement this method.")

    def get_active_requests(self) -> int:
        return self.active_requests

    async def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.active_requests += 1
        try:
            # Simulate API call for now
            # async with httpx.AsyncClient() as client:
            #     headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            #     response = await client.post(f"{self.base_url}/completions", json=payload, headers=headers, timeout=30.0)
            #     response.raise_for_status()
            #     return response.json()
            print(f"MOCK LLM Request ({self.model_name}): Payload: {str(payload)[:200]}...")
            await asyncio.sleep(0.5) # Simulate network latency
            
            # Mock response structure (varies by API)
            if "generate_headings" in payload.get("prompt", "").lower():
                 num_slides_requested = int(payload.get("prompt", "").split(" ")[1]) if "Generate" in payload.get("prompt","") else 5
                 return {"choices": [{"text": "\n".join([f"{i+1}. Mock Heading {i+1} for {self.model_name}" for i in range(num_slides_requested)])}]}

            return {"choices": [{"text": f"Mock content from {self.model_name} for prompt: '{payload.get('prompt', '')[:50]}...' Styles: temp={payload.get('temperature',0.7)}, max_tokens={payload.get('max_tokens',100)}"}]}

        except httpx.HTTPStatusError as e:
            print(f"API Error for {self.model_name}: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            print(f"Request Error for {self.model_name}: {str(e)}")
            raise
        finally:
            self.active_requests -= 1


# --- Specific LLM Implementations (Mocked) ---
class GeminiAPI(BaseLLMAPI):
    def __init__(self):
        super().__init__(settings.GEMINI_API_KEY, "https://generativelanguage.googleapis.com/v1beta/models", "gemini-pro:generateContent") # Example endpoint

    async def generate_text(self, prompt: str, max_tokens: int, temperature: float = 0.7) -> str:
        if not self.api_key: return "Gemini API key not configured. Returning mock data."
        
        # Gemini API has a specific request structure
        payload = {
            "contents": [{"parts":[{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens 
            }
        }
        # Actual Gemini prompt might need to consider total tokens for request+response
        # For simplicity, this mock assumes max_tokens is for output.
        
        response_data = await self._make_request(payload)
        # Actual parsing of Gemini response:
        # return response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error or empty response")
        return response_data.get("choices", [{}])[0].get("text", "Mock Gemini Error")


class GPT_API(BaseLLMAPI): # e.g., OpenAI
    def __init__(self):
        super().__init__(settings.GPT_API_KEY, "https://api.openai.com/v1", "gpt-3.5-turbo-instruct") # Or gpt-4 etc.

    async def generate_text(self, prompt: str, max_tokens: int, temperature: float = 0.7) -> str:
        if not self.api_key: return "GPT API key not configured. Returning mock data."
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response_data = await self._make_request(payload)
        return response_data.get("choices", [{}])[0].get("text", "Mock GPT Error").strip()

class DeepSeekAPI(BaseLLMAPI):
    def __init__(self):
        super().__init__(settings.DEEPSEEK_API_KEY, "https://api.deepseek.com/v1", "deepseek-coder") # Example model

    async def generate_text(self, prompt: str, max_tokens: int, temperature: float = 0.7) -> str:
        if not self.api_key: return "DeepSeek API key not configured. Returning mock data."
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response_data = await self._make_request(payload)
        return response_data.get("choices", [{}])[0].get("text", "Mock DeepSeek Error").strip()

class MistralAPI(BaseLLMAPI):
    def __init__(self):
        super().__init__(settings.MISTRAL_API_KEY, "https://api.mistral.ai/v1", "mistral-small-latest") # Example model

    async def generate_text(self, prompt: str, max_tokens: int, temperature: float = 0.7) -> str:
        if not self.api_key: return "Mistral API key not configured. Returning mock data."
        # Mistral API might use a chat completions structure similar to OpenAI
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response_data = await self._make_request(payload) # Assuming _make_request is adapted or this API returns similar structure
        # Actual parsing for chat completion:
        # return response_data.get("choices", [{}])[0].get("message", {}).get("content", "Mock Mistral Error").strip()
        return response_data.get("choices", [{}])[0].get("text", "Mock Mistral Error - adapt for chat structure").strip()


# --- Factory to get LLM instances ---
AVAILABLE_LLMS = {
    "gemini": GeminiAPI,
    "gpt": GPT_API,
    "deepseek": DeepSeekAPI,
    "mistral": MistralAPI,
}

# Initialize instances (could be done on demand)
LLM_INSTANCES = {name: klass() for name, klass in AVAILABLE_LLMS.items()}

async def generate_with_llm(
    llm_name: str,
    prompt: str,
    max_tokens: int,
    temperature: float = 0.7,
    retry_attempts: int = 2,
    backoff_factor: float = 0.5 # seconds
) -> str:
    instance = LLM_INSTANCES.get(llm_name)
    if not instance:
        raise ValueError(f"LLM '{llm_name}' not found or configured.")

    if not instance.api_key:
        print(f"Warning: API key for {llm_name} is not configured. Using mock response.")
        # Fallback to a generic mock if key is missing, even if class has mock logic
        return f"Mock response: API key for {llm_name} missing. Prompt: '{prompt[:30]}...'"

    current_attempt = 0
    while current_attempt <= retry_attempts:
        try:
            return await instance.generate_text(prompt, max_tokens, temperature)
        except httpx.HTTPStatusError as e:
            # Specific error handling, e.g., rate limits (429)
            if e.response.status_code == 429 or e.response.status_code >= 500: # Retry on rate limit or server errors
                print(f"LLM API error for {llm_name} (Attempt {current_attempt+1}/{retry_attempts+1}): {e.response.status_code}. Retrying...")
                current_attempt += 1
                if current_attempt > retry_attempts:
                    raise # Max retries reached
                await asyncio.sleep(backoff_factor * (2 ** (current_attempt -1))) # Exponential backoff
            else: # Non-retryable client-side HTTP errors
                raise
        except Exception as e: # Other errors like network issues
            print(f"Error during LLM call for {llm_name} (Attempt {current_attempt+1}/{retry_attempts+1}): {str(e)}. Retrying...")
            current_attempt += 1
            if current_attempt > retry_attempts:
                raise # Max retries reached
            await asyncio.sleep(backoff_factor * (2 ** (current_attempt-1)))
    raise Exception(f"Failed to generate text with {llm_name} after {retry_attempts+1} attempts.")