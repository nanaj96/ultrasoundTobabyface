import streamlit as st
import requests
from PIL import Image
import io
import base64

# ComfyUI API endpoint
COMFYUI_API_URL = "https://d0gu9c5gl5yzxr-8188.proxy.runpod.net/"  # Replace with actual URL

st.title("Ultrasound to Baby Face AI")

# UI Layout
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if st.button("Generate Image") and uploaded_file:
        image_bytes = uploaded_file.read()
        files = {"image": ("input.jpg", image_bytes, "image/jpeg")}
        
        with st.spinner("Generating Image... ⏳"):
            response = requests.post(COMFYUI_API_URL, files=files)

        if response.status_code == 200:
            output_images = response.json().get("images", [])
            st.session_state["generated_images"] = []

            for img_data in output_images:
                # Agar image base64 me ho
                img_bytes = base64.b64decode(img_data)
                img = Image.open(io.BytesIO(img_bytes))
                st.session_state["generated_images"].append(img)

        else:
            st.error("Failed to generate image. Please try again.")

with col2:
    if "generated_images" in st.session_state and st.session_state["generated_images"]:
        st.image(st.session_state["generated_images"], caption="Generated Images", width=150)
    else:
        st.write("Generated images will appear here.")
