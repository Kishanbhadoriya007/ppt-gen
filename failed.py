# generator = pipeline('text-generation', model='distilgpt2')

# generator('What is the meaning of life', max_length=30, num_return_sequences=3)

# warnings.filterwarnings("ignore", message="Special tokens have been added in the vocabulary")

# # Suppress the warning about special tokens
# logging.getLogger('transformers.tokenization_utils_base').setLevel(logging.ERROR)

# # Your existing code continues here...

# tokenizer = transformers.AutoTokenizer.from_pretrained("Nexusflow/Starling-LM-7B-beta")

# model = transformers.AutoModelForCausalLM.from_pretrained("Nexusflow/Starling-LM-7B-beta")

# def generate_response(prompt):
#     input_ids = tokenizer(prompt, return_tensors="pt").input_ids
#     outputs = model.generate(
#         input_ids,
#         max_length=256,
#         pad_token_id=tokenizer.pad_token_id,
#         eos_token_id=tokenizer.eos_token_id,
#     )
#     response_ids = outputs[0]
#     response_text = tokenizer.decode(response_ids, skip_special_tokens=True)
#     return response_text