import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Image Opacity Mixer",
    page_icon="🖼️",
    layout="centered"
)

def blend_images(img1, img2, opacity):
    # Ensure both images have the same size
    if img1.shape != img2.shape:
        raise ValueError("Both images must have the same dimensions for blending.")

    # Perform image blending based on opacity
    blended_image = cv2.addWeighted(img1, opacity, img2, 1 - opacity, 0)

    return blended_image

def main():
    st.title("Image Opacity Mixer")

    # Upload image through Streamlit
    uploaded_image1 = st.file_uploader("Upload Image 1", ["jpg", "jpeg", "png", "webp"])
    uploaded_image2 = st.file_uploader("Upload Image 2", ["jpg", "jpeg", "png", "webp"])

    if uploaded_image1 is not None and uploaded_image2 is not None:
        # Read the uploaded images
        image1 = cv2.imdecode(np.frombuffer(uploaded_image1.read(), np.uint8), 1)
        image2 = cv2.imdecode(np.frombuffer(uploaded_image2.read(), np.uint8), 1)

        # Convert images to RGB format
        image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

        # Resize images to have the same dimensions
        width, height = min(image1.shape[1], image2.shape[1]), min(image1.shape[0], image2.shape[0])
        image1_rgb = cv2.resize(image1_rgb, (width, height))
        image2_rgb = cv2.resize(image2_rgb, (width, height))

        # Display images in the first two columns with reduced size
        col1, col2 = st.columns(2)
        col1.image(image1_rgb, caption="Image 1 (RGB)", use_column_width=True, width=200)
        col2.image(image2_rgb, caption="Image 2 (RGB)", use_column_width=True, width=200)

        # Create an empty space for opacity slider
        opacity_placeholder = st.empty()

        # Combine images using the opacity slider
        opacity_slider = opacity_placeholder.slider("Opacity", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

        # Resize images to the same dimensions for blending
        image1_for_blend = cv2.resize(image1, (width, height))
        image2_for_blend = cv2.resize(image2, (width, height))

        # Combine images using the opacity slider
        blended_image = blend_images(image1_for_blend, image2_for_blend, opacity_slider)
        blended_image_rgb = cv2.cvtColor(blended_image, cv2.COLOR_BGR2RGB)

        # Display the blended image directly under the slider with reduced size
        st.image(blended_image_rgb, caption=f"Blended Image (Opacity: {opacity_slider})", use_column_width=True, width=400)

        # Button to download the blended image
        if st.button("Download Blended Image"):
            blended_image_pil = Image.fromarray(blended_image_rgb)
            st.download_button(
                label="Download Blended Image",
                data=blended_image_pil,
                file_name="blended_image.png",
                key="download_button"
            )

    else:
        st.warning("Please upload two images to get started.")

if __name__ == "__main__":
    main()
