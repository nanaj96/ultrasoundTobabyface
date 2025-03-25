import streamlit as st
import requests
from PIL import Image
import io
import base64

# ✅ Correct ComfyUI API endpoint
COMFYUI_API_URL = "https://uc5a0pbk8d04m5-8188.proxy.runpod.net/"  # Replace with your correct RunPod IP

st.title("Ultrasound to Baby Face AI")

# UI Layout
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Image"):
        if uploaded_file:
            image_bytes = uploaded_file.read()
            
            # ✅ Encode image to base64
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")

            # ✅ Correct Payload for ComfyUI API
            payload = {
                "prompt": {
                    "0": {
                        "inputs": {
                            "image": {
                                "image": encoded_image,
                                "type": "image"
                            }
                        }
                    }
                }
            }

            headers = {"Content-Type": "application/json"}

            with st.spinner("Generating Image... ⏳"):
                try:
                    # ✅ Correct API request
                    response = requests.post(COMFYUI_API_URL, json=payload, headers=headers)

                    if response.status_code == 200:
                        output_images = response.json().get("images", [])
                        st.session_state["generated_images"] = []

                        for img_data in output_images:
                            # ✅ Decode base64 response to image
                            img_bytes = base64.b64decode(img_data)
                            img = Image.open(io.BytesIO(img_bytes))
                            st.session_state["generated_images"].append(img)

                        st.success("✅ Image generated successfully!")

                    else:
                        st.error("❌ Failed to generate image. Please try again.")

                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.warning("⚠️ Please upload an image first.")

with col2:
    if "generated_images" in st.session_state and st.session_state["generated_images"]:
        st.image(st.session_state["generated_images"], caption="Generated Images", width=150)
    else:
        st.write("Generated images will appear here.")
