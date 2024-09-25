import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="Image Contours", 
    page_icon="⌨",
    layout="centered"
)

# Function to process the uploaded image
def process_image(uploaded_file):
    # Check if any file is uploaded
    if uploaded_file is not None:
        # Read the uploaded image
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(
            image=thresh,
            mode=cv2.RETR_TREE,
            method=cv2.CHAIN_APPROX_NONE
        )

        # Draw contours on the original image
        image_copy = image.copy()
        cv2.drawContours(
            image=image_copy,
            contours=contours,
            contourIdx=-1,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_AA
        )

        # Display the results using st.image
        st.image(image_copy, channels="BGR", caption="Contours Image", use_column_width=True)
    else:
        st.warning("Please upload an image.")

# Streamlit app
def main():
    st.title("Contours Detection with Streamlit")

    # Upload an image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Process and display the image
    process_image(uploaded_file)

if __name__ == "__main__":
    main()