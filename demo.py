from pptx import Presentation

from transformers import pipeline

generator = pipeline("text-generation", model="distilgpt2")

result = generator(
    
    "PPT-generator presentation",
    max_length=50,
    num_return_sequences=2,          
)
print(result)




# single_turn_prompt = f"GPT4 Correct User: {prompt}<|end_of_turn|>GPT4 Correct Assistant:"
# response_text = generate_response(single_turn_prompt)
# print("Response:", response_text)