import cv2
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Image Circle Detection", 
    page_icon="⌨",
    layout="wide"
)

# Function to detect circles and draw them on the image
def detect_and_draw_circles(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 10)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])

            # Circle center
            cv2.circle(image, center, 1, (0, 100, 100), 3)

            # Circle outline
            radius = i[2]
            cv2.circle(image, center, radius, (255, 0, 255), 3)

# Streamlit app
def main():
    st.title("Image Circle Detection")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg", "webp"])

    if uploaded_file is not None:
        # Read the image
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)

        # Process the image
        detect_and_draw_circles(image)

        # Display the result
        st.image(image, channels="BGR", caption="Processed Image", use_column_width=True)

if __name__ == "__main__":
    main()
