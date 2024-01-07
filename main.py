from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize chat history for text processing if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to get Gemini response for text processing
def get_text_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro") 
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# Function to get Gemini response for image processing
def get_image_gemini_response(input_text, uploaded_image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input_text != "":
       response = model.generate_content([input_text, uploaded_image])
    else:
       response = model.generate_content(uploaded_image)
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title="Multi-Modal Gemini App")
st.header("RT-Gemini LLM Application")

# Sidebar and user inputs for text and image processing
option = st.sidebar.radio("Select Mode", ["Text Processing", "Image Processing"])
input_text = ""
uploaded_image = None

if option == "Text Processing":
    input_text = st.text_input("Input for Text: ", key="input_text")
    submit_text = st.button("Ask the question for Text")

    if submit_text and input_text:
        text_response = get_text_gemini_response(input_text)
        st.subheader("The Response for Text is")
        for chunk in text_response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

elif option == "Image Processing":
    input_text = st.text_input("Input Prompt for Image: ", key="input_image")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        uploaded_image = Image.open(uploaded_image)
        st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
    
    submit_image = st.button("Tell me about the image")

    if submit_image:
        image_response = get_image_gemini_response(input_text, uploaded_image)
        st.subheader("The Response for Image is")
        st.write(image_response)

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
