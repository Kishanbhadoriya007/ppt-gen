from flask import Flask, request, jsonify
from pptx import Presentation
from pptx.util import Inches
from pptx.dml.color import RGBColor
from transformers import pipeline
import firebase_admin  
from firebase_admin import db, credentials

# Initialize Flask app
app = Flask(__name__)

# Replace with your Firebase project credentials (obtained from Firebase console)
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, ("databaseURL":"https://ppt-generator-b5032-default-rtdb.asia-southeast1.firebasedatabase.app/"))
{
    "type": "...",
    "project_id": "...",
    "private_key": "...",
    "client_email": "...",
    "client_id": "..."
}

# Initialize Firebase app
firebase_admin.initialize_app(cred)
db = firebase_admin.firestore.client()  # Access Firestore database

# Text generation pipeline (replace with your preferred method)
generator = pipeline("text-generation", model="openai-community/gpt2")


def generate_slides(title, slides, theme_color, image_data=None):
    pr = Presentation()

    # Set theme color (if provided)
    if theme_color:
        try:
            color = RGBColor.from_string(theme_color)
            pr.slide_master.designs[0].slide_layouts[0].shapes[0].fill.solid()
            pr.slide_master.designs[0].slide_layouts[0].shapes[0].fill.fore_color.rgb = color
        except ValueError:
            print("Invalid theme color name.")

    generated_texts = []
    for prompt in slides:
        generated_text = generator(prompt, max_length=250, num_return_sequences=1, truncation=True)[0]['generated_text']
        generated_texts.append(generated_text)

    for i, text in enumerate(generated_texts):
        slide = pr.slides.add_slide(pr.slide_layouts[0])
        title_shape = slide.shapes.title
        subtitle_placeholder = slide.placeholders[1]

        title_shape.text = f"{title} - Page {i+1}"
        subtitle_placeholder.text_frame.paragraphs[0].text = text

        # Add image functionality (replace with actual logic)
        if image_data:
            try:
                pic = slide.shapes.add_picture(image_data, left=Inches(1), top=Inches(2), width=Inches(3))
            except FileNotFoundError:
                print("Image not found.")

    # Save to presentation and potentially store in Firebase
    presentation_data = pr.slides[0].slide_width, pr.slides[0].slide_height, pr.save('generated_presentation.pptx')
    db.collection('presentations').add({'title': title, 'data': presentation_data})  # Store presentation metadata

    return "Presentation generated successfully!"


@app.route('/generate', methods=['POST'])
def generate_presentation():
    data = request.form
    title = data.get('title')
    slides = data.getlist('slide')
    theme_color = data.get('theme-color')
    image = request.files.get('image')  # Access uploaded image

    if image:
        image_data = image.read()  # Read image data
    else:
        image_data = None

    response = generate_slides(title, slides, theme_color, image_data)
    return jsonify({'message': response})


if __name__ == '__main__':
    app.run(debug=True)
