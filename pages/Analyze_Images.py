import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
st.title("Image Analyzer")

gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key= gemini_api_key)


# Function to analyze image with Gemini
def analyze_image(image, prompt="Analyze this image and describe what you see in detail."):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content([prompt, image], stream=True)
    return response


st.set_page_config(
    page_title="Image Analyzer",
    page_icon="📸"
)

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# File uploader for images
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
    help="Upload an image to analyze"
)

# Optional: Custom prompt input
custom_prompt = st.text_area(
    "Analysis prompt (optional)",
    value="Analyze this image and describe what you see in detail.",
    help="Customize what you want to know about the image"
)

# Analyze button
if st.button("Analyze Image", disabled=uploaded_file is None):
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Show analysis in progress
        with st.spinner("Analyzing image..."):
            try:
                # Analyze the image
                streaming_response = analyze_image(image, custom_prompt)

                # Display the analysis
                st.subheader("Analysis Results:")
                placeholder = st.empty()
                full_response = ""

                for chunk in streaming_response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + " ")

                placeholder.markdown(full_response)

                # Add to history
                st.session_state.analysis_history.append({
                    "image_name": uploaded_file.name,
                    "prompt": custom_prompt,
                    "response": full_response
                })

            except Exception as e:
                st.error(f"Error analyzing image: {e}")