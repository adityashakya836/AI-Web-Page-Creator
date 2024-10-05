import streamlit as st 
import google.generativeai as genai 
import json
from PIL import Image

config_file_path = 'config.json'
with open(config_file_path, 'r') as file:
    config_data = json.load(file)

GOOGLE_API_KEY = config_data['GOOGLE_API_KEY']

genai.configure(api_key = GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# Load the model
def get_gemini_response(input, image):
    """
    Input: What I want the assistant to do.
    Prompt: What message I want
    """
    response = model.generate_content([input, image[0]])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')

# Setting streamlit app
st.set_page_config(page_title = 'AI Web Page Maker')
st.header("Web Page Maker")
uploaded_file = st.file_uploader("Choose an image of the webpage", type = ['jpg', 'jpeg', 'png'])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = "Uploaded Image", use_column_width = True)

submit = st.button('Create Code')

input_prompt = """
You are a specialized assistant with an advanced understanding of web page designs, images, and hand-drawn sketches. Whether it's a wireframe, a designed web page image, or a conceptual illustration, your task is to accurately interpret and write the corresponding HTML and CSS code to bring that design to life. Focus on responsive design, clean structure, and accurate representation of visual elements. Ensure to include:

HTML structure that organizes the page's content and semantic elements.
CSS styling to ensure the page looks as close to the design as possible, including typography, colors, layouts, hover effects, and responsiveness.
Custom CSS animations or transitions if indicated in the design.
Ensure the final code reflects best practices in web development with modern techniques like Flexbox/Grid, media queries for responsiveness, and accessibility considerations.
"""

# If submit is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("The Reponse is")
    st.write(response)