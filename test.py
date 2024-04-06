from pptx import Presentation
from pptx.util import Inches
from transformers import pipeline

generator = pipeline("text-generation", model="openai-community/gpt2")

title = input("Enter title: ")

# Define list of prompts for slides
prompts = [
    input("Describe the topic for slide 1: "),
    input("Describe the topic for slide 2: "),
    input("Describe the topic for slide 3: "),
    input("Describe the topic for slide 4: ")
]

pr1 = Presentation()

# Initialize list to store generated texts
generated_texts = []

for i, prompt in enumerate(prompts):
    generated_text = generator(prompt, max_length=250, num_return_sequences=1, truncation=True)[0]['generated_text']

    # Store generated text in a list
    generated_texts.append(generated_text)

    slide = pr1.slides.add_slide(pr1.slide_layouts[0])  # Use title and subtitle layout
    title_shape = slide.shapes.title
    subtitle_placeholder = slide.placeholders[1]  # Access the subtitle placeholder

    title_shape.text = f"{title} - Page {i+1}"  # Add page numbering to title

    # Loop through generated text list and add paragraphs
    for point in generated_texts[i].split("\n"):
        paragraph = subtitle_placeholder.text_frame.add_paragraph()
        paragraph.text = point

# Add bullet points to each slide (optional)
# ... (follow similar logic for adding bullet points if needed)

pr1.save("ppt-gen-multiple.pptx")
