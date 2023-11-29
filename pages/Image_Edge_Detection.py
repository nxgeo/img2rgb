import streamlit as st
import cv2
import numpy as np
from pandas import DataFrame
from PIL import Image

st.set_page_config(
    page_title="Image Edge Detection", 
    page_icon="⌨",
    layout="wide"
)

def edge_detection(image, divisor=1):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Sobel operator for edge detection
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Compute the gradient magnitude
    gradient_mag = np.sqrt(sobel_x**2 + sobel_y**2)

    # Normalize the gradient magnitude
    gradient_mag = (gradient_mag / divisor).astype(np.uint8)

    return gradient_mag

def get_pixel_data(image):
    if image.mode == 'RGB':
        pixel_data = [
            [image.getpixel((x, y)) for x in range(image.width)]
            for y in range(image.height)
        ]
    elif image.mode == 'L':
        pixel_data = [
            [image.getpixel((x, y)) for x in range(image.width)]
            for y in range(image.height)
        ]
    else:
        raise ValueError("Unsupported image mode")

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

        # Use st.columns to create two columns
        col1, col2 = st.columns(2)

        # Display the original image in the first column
        col1.image(img_rgb, caption="Original Image", use_column_width=True)

        # Get and display pixel data for the original image in the first column
        with col1:
            st.subheader("Pixel Data Original")
            st.dataframe(get_pixel_data(img_rgb))

        # Perform edge detection with a divisor
        divisor = st.slider("Divisor", min_value=1, max_value=10, value=1)
        edges = edge_detection(image, divisor)

        # Display the edge detection result in the second column
        col2.image(edges, caption="Edge Detection Result", use_column_width=True)

        # Get and display pixel data for the edge detection result in the second column
        with col2:
            st.subheader("Pixel Data Result")
            st.dataframe(get_pixel_data(Image.fromarray(edges)))
    else:
        st.warning("Please upload an image.")

if __name__ == "__main__":
    main()
