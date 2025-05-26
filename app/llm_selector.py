# app/llm_selector.py
import random
from typing import Dict, List, Optional, Callable, Awaitable

from .llm_integrations import LLM_INSTANCES, BaseLLMAPI # Assuming LLM_INSTANCES is a dict of initialized APIs

# --- Configuration for LLM Selection ---
# Probabilities should sum to 1 for each task type if using simple probability.
# Structure: { "task_type": {"llm_name": probability, ...} }
LLM_PROBABILITIES = {
    "default": { # Fallback probabilities
        "gemini": 0.4,
        "gpt": 0.3,
        "deepseek": 0.15,
        "mistral": 0.15,
    },
    "heading_generation": { # Specific task probabilities
        "gemini": 0.5,
        "gpt": 0.4,
        "mistral": 0.1, # Example: Mistral might be good for shorter, creative tasks
    },
    "content_generation": {
        "gpt": 0.4,
        "gemini": 0.3,
        "deepseek": 0.2, # Example: Deepseek Coder might be good if content is code-related
        "mistral": 0.1,
    }
}

# This needs to be managed if you have stateful LLM_INSTANCES
# For simplicity, assume LLM_INSTANCES is available from llm_integrations
# from .llm_integrations import LLM_INSTANCES

def select_llm_for_task(task_type: str = "default") -> BaseLLMAPI:
    """
    Selects an LLM based on pre-defined probabilities and current availability (conceptual).
    """
    task_probabilities = LLM_PROBABILITIES.get(task_type, LLM_PROBABILITIES["default"])
    
    available_llms = []
    llm_weights = []

    for llm_name, instance in LLM_INSTANCES.items():
        if instance.api_key and llm_name in task_probabilities: # Check if API key exists and LLM is in prob dict
            # Conditional probability: Prioritize LLMs with fewer active requests
            # This is a simple heuristic; real-world might need more sophisticated load balancing.
            active_reqs = instance.get_active_requests()
            
            # Adjust weight: higher probability for less busy LLMs
            # The adjustment factor needs tuning. Example:
            weight_adjustment = 1 / (1 + active_reqs * 0.5) # Penalize more for more requests
            
            adjusted_prob = task_probabilities[llm_name] * weight_adjustment
            
            available_llms.append(llm_name)
            llm_weights.append(adjusted_prob)

    if not available_llms:
        # Fallback if no LLMs are available (e.g., all keys missing or no suitable LLMs for task)
        print("Warning: No LLMs available with configured API keys for selection. Using a default mock behavior.")
        # You might return a default mock LLM instance here or raise an error
        # For now, let's try to pick any configured LLM if the sophisticated selection fails.
        configured_llms = [name for name, inst in LLM_INSTANCES.items() if inst.api_key]
        if configured_llms:
            chosen_llm_name = random.choice(configured_llms)
            return LLM_INSTANCES[chosen_llm_name]
        else:
            # If truly no LLM is configured at all, this is a critical issue.
            # Fallback to a dummy/mock instance not in LLM_INSTANCES if you have one, or raise.
            # For this example, we'll assume at least one mock in LLM_INSTANCES can be picked even without key for mock mode.
            # This part would need a more robust "no LLM available" handling.
            print("CRITICAL: No LLMs with API keys configured, and fallback selection failed.")
            # Returning the first LLM instance regardless of key for purely mock operation:
            return list(LLM_INSTANCES.values())[0]


    # Normalize weights if they don't sum to 1 (though random.choices handles non-normalized weights)
    # total_weight = sum(llm_weights)
    # normalized_weights = [w / total_weight for w in llm_weights] if total_weight > 0 else [1/len(llm_weights)]*len(llm_weights)

    if not llm_weights or sum(llm_weights) == 0: # Handle case where all adjusted probabilities become zero
        if available_llms: # If there are available LLMs but weights are zero (e.g. all probs were zero)
            chosen_llm_name = random.choice(available_llms)
        else: # Should not happen if previous check for available_llms passed
            raise Exception("No LLMs available for selection after weighting.")
    else:
        chosen_llm_name = random.choices(available_llms, weights=llm_weights, k=1)[0]
    
    print(f"Selected LLM for task '{task_type}': {chosen_llm_name} (Active: {LLM_INSTANCES[chosen_llm_name].get_active_requests()})")
    return LLM_INSTANCES[chosen_llm_name]


async def get_llm_response(
    prompt: str,
    max_tokens: int,
    task_type: str = "default", # e.g., "heading_generation", "content_generation"
    temperature: float = 0.7,
    style_tone: Optional[str] = None, # Passed to prompt optimizer, not directly to LLM selector
    content_format: Optional[str] = None # Passed to prompt optimizer
) -> str:
    """
    High-level function to get a response from a selected LLM.
    """
    # 1. Select LLM
    selected_llm_instance = select_llm_for_task(task_type) # This returns an instance of BaseLLMAPI
    
    # 2. (Prompt optimization can happen before or after LLM selection,
    #    or even be specific to the LLM chosen, but for simplicity, we assume
    #    the prompt passed here is already somewhat optimized or ready).
    #    The actual call to prompt_optimizer is in services.py before this.

    # 3. Generate text using the selected LLM's method
    #    The `generate_with_llm` function in `llm_integrations` now expects llm_name.
    #    We need to get the name of the selected LLM.
    llm_name_key = None
    for name, instance in LLM_INSTANCES.items():
        if instance == selected_llm_instance:
            llm_name_key = name
            break
    
    if not llm_name_key:
        raise Exception("Could not determine the name of the selected LLM instance.")

    return await llm_integrations.generate_with_llm(
        llm_name=llm_name_key,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )