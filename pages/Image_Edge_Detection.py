import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="Image Steganography", 
    page_icon="⌨",
    layout="wide"
)

def edge_detection(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    return edges

def main():
    st.title("Image Edge Detection App")

    # Upload image through Streamlit
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        # Read the uploaded image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        
        st.image(image, caption="Original Image", use_column_width=True)
        
        # Perform edge detection
        edges = edge_detection(image)
        
        st.image(edges, caption="Edge Detection Result", use_column_width=True)
    else:
        st.warning("Please upload an image.")

        
if __name__ == "__main__":
    main()
