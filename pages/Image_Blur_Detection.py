import cv2
import numpy as np
import streamlit as st
from matplotlib import pyplot as plt
from io import BytesIO

# Function to detect blur
def detect_blur(image):
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), 1)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Fourier Transform
    (h, w) = image.shape
    (cX, cY) = (int(w/2.0), int(h/2.0))
    fft = np.fft.fft2(image)
    fftShift = np.fft.fftshift(fft)

    magnitude = 20 * np.log(np.abs(fftShift))

    # Plot original image
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption='Original Image', use_column_width=True)

    # Plot input image and magnitude spectrum
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.imshow(img, cmap='gray')
    ax1.set_title('Input Image')
    ax1.axis('off')

    ax2.imshow(magnitude, cmap='gray')
    ax2.set_title('Magnitude Spectrum')
    ax2.axis('off')

    st.pyplot(fig)

    # Detect blur
    size = 60
    fftShift[cY - size:cY + size, cX - size:cX + size] = 0
    fftShift = np.fft.ifftshift(fftShift)
    recon = np.fft.ifft2(fftShift)
    magnitude_recon = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude_recon)

    st.write(f"Mean value of magnitude spectrum: {mean}")

    thres = 10
    if mean <= thres:
        st.write("Blur Image")
    else:
        st.write("No Blur")


# Streamlit app
st.title('Blur Detection App')
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    detect_blur(uploaded_file)
