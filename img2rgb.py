# Pixel Data RGB
from pandas import DataFrame
from PIL import Image
import streamlit as st

# Histogram
import cv2
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd

st.set_page_config(
    page_title="img2rgb", 
    page_icon="🌈",
    layout="wide"
)

st.title("🌈 Image to RGB")

uploaded_image = st.file_uploader("Upload an image", ["jpg", "jpeg", "png", "webp"])

if uploaded_image is not None:
    _, centered_column, _ = st.columns(3)
    centered_column.image(uploaded_image, width=300)

    image = Image.open(uploaded_image).convert("RGB")

    image_attrs = {
        "Filename": uploaded_image.name,
        "Type": uploaded_image.type,
        "Mode": image.mode,
        "Resolution": f"{image.width} × {image.height}",
    }
    st.header("Image Attribute")
    st.table(image_attrs)

    with st.spinner("Getting RGB value for each pixel..."):
        pixel_rgbs = [
            [image.getpixel((x, y)) for x in range(image.width)]
            for y in range(image.height)
        ]

    with st.spinner("Converting pixel data to DataFrame..."):
        st.header("Pixel Data RGB")
        df = DataFrame(pixel_rgbs)
        df.index += 1
        df.columns += 1
        df.index.name = "Px"

    with st.spinner("Displaying result..."):
        st.dataframe(df)
        st.caption("Note: Each cell represents the RGB value of a pixel in the image.")

    with st.spinner("Displaying RGB histogram...."):

        st.header("RGB Histogram")
        # Read the uploaded image

        # Convert Image to RGB
        img_rgb = np.array(image)

        # Calculate RGB histogram
        r_hist = cv2.calcHist([img_rgb], [0], None, [256], [0, 256])
        g_hist = cv2.calcHist([img_rgb], [1], None, [256], [0, 256])
        b_hist = cv2.calcHist([img_rgb], [2], None, [256], [0, 256])

        # Determine fig
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

        # Plot RGB histograms using Matplotlib
        ax1.plot(r_hist, color='red', label='Red', alpha=0.7, linewidth=2)
        ax1.plot(g_hist, color='green', label='Green', alpha=0.7, linewidth=2)
        ax1.plot(b_hist, color='blue', label='Blue', alpha=0.7, linewidth=2)
        ax1.set_xlabel('Pixel Value', fontsize=14)
        ax1.legend()
        ax1.grid(True)

        # Show RGB image
        ax2.imshow(img_rgb)
        ax2.axis('off')

        # Display the plot in Streamlit
        st.pyplot(fig)

        # Pixel data to DataFrame
        df_rgb = pd.DataFrame(img_rgb.reshape(-1, 3), columns=["Red", "Green", "Blue"])

        st.header("Pixel Data (RGB)")
        st.dataframe(df_rgb)

    with st.spinner("Displaying Grayscale Histogram"):

        st.header("Grayscale Histogram")
        
        # Read uploaded image and convert to greyscale data
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # Calculate grayscale histogram
        gray_hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])

        # Determine fig
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

        ax1.plot(gray_hist, color='gray', label='Grayscale', alpha=0.7, linewidth=2)
        ax1.set_xlabel('Pixel Value', fontsize=14)
        ax1.legend()
        ax1.grid(True)

        # Show grayscale image
        ax2.imshow(img_gray, cmap='gray')
        ax2.axis('off')

        # Display the plot in Streamlit
        st.pyplot(fig)
