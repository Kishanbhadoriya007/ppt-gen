# app/prompt_optimizer.py
from typing import List
from .schemas import SlideContentRequest

def optimize_heading_generation_prompt(main_topic: str, num_slides: int) -> str:
    return (
        f"Generate {num_slides} concise and engaging slide headings for a presentation about '{main_topic}'. "
        f"Each heading should be suitable for a single PowerPoint slide. "
        f"Return the headings as a numbered list. Do not include any other text or explanations."
    )


def optimize_slide_content_prompt(
    heading: str,
    main_topic: str,
    style_tone: str = "neutral",
    content_format: str = "bullet_points", # "bullet_points", "summary", "paragraph"
    max_tokens: int = 250
) -> str:
    
    format_instruction = ""
    if content_format == "bullet_points":
        format_instruction = "Present the key information as concise bullet points (3-5 points typically). Each bullet point should be on a new line, starting with a hyphen or asterisk."
    elif content_format == "summary":
        format_instruction = f"Provide a brief summary of the key information, approximately {max_tokens // 20}-{max_tokens // 15} sentences long." # Rough estimate
    elif content_format == "paragraph":
        format_instruction = f"Write a detailed paragraph. Aim for around {max_tokens} tokens."

    style_instruction = ""
    if style_tone == "formal":
        style_instruction = "Use a formal and professional tone."
    elif style_tone == "casual":
        style_instruction = "Use a casual and conversational tone."
    elif style_tone == "academic":
        style_instruction = "Use an academic tone, citing information if it were from a source (though you don't need to invent sources here)."
    
    prompt = (
        f"For a PowerPoint slide titled '{heading}' within a presentation about '{main_topic}':\n"
        f"{format_instruction}\n"
        f"{style_instruction}\n"
        f"The content should be informative and directly relevant to the heading. "
        f"Ensure the generated content is within approximately {max_tokens} tokens. " # LLMs understand "tokens" to varying degrees
        f"Focus on clarity and readability for a presentation slide. Avoid overly complex sentences. "
        f"Do not include the heading itself in the response, only the content for the slide body."
    )
    return prompt

def count_tokens_simple(text: str) -> int:
    """
    A very basic placeholder for token counting.
    Real token counting requires the specific tokenizer for the LLM being used.
    This is a rough estimate (words + punctuation).
    """
    return len(text.split()) + text.count(',') + text.count('.') # very naive