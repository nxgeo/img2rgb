import streamlit as st
import cv2
import numpy as np
from pandas import DataFrame
from PIL import Image

st.set_page_config(
    page_title="Image Edge Detection App", 
    page_icon="⌨",
    layout="wide"
)

def edge_detection(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    return edges

def get_pixel_data(image):
    pixel_data = [
        [image.getpixel((x, y)) for x in range(image.width)]
        for y in range(image.height)
    ]
    df = DataFrame(pixel_data)
    df.index += 1
    df.columns += 1
    df.index.name = "Px"
    
    return df

def main():
    st.title("Image Edge Detection App")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        # Read the uploaded image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        img_rgb = Image.open(uploaded_file).convert("RGB")
        img_gray = Image.open(uploaded_file).convert("L")

        # Use st.columns to create two columns
        col1, col2 = st.columns(2)

        # Display the original image in the first column
        col1.image(image, caption="Original Image", use_column_width=True)

        # Get and display pixel data for the original image in the first column
        with col1:
            st.subheader("Pixel Data Original")
            st.dataframe(get_pixel_data(img_rgb))

        # Perform edge detection
        edges = edge_detection(image)

        # Display the edge detection result in the second column
        col2.image(edges, caption="Edge Detection Result (Grayscale)", use_column_width=True)

        # Get and display pixel data for the edge detection result in the second column
        with col2:
            st.subheader("Pixel Data Result")
            st.dataframe(get_pixel_data(img_gray))
    else:
        st.warning("Please upload an image.")

if __name__ == "__main__":
    main()
