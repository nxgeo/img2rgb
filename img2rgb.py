from pandas import DataFrame
from PIL import Image
import streamlit as st

st.title("Image to RGB")

uploaded_image = st.file_uploader("Upload an image", ["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")

    st.image(
        uploaded_image, f"{uploaded_image.name}, {image.width}×{image.height}", 200
    )

    with st.spinner("Getting RGB value for each pixel..."):
        pixel_rgbs = [
            [image.getpixel((x, y)) for x in range(image.width)]
            for y in range(image.height)
        ]

    with st.spinner("Converting pixel data to DataFrame..."):
        df = DataFrame(pixel_rgbs)
        df.index += 1
        df.columns += 1

    with st.spinner("Displaying result..."):
        st.dataframe(df)
        st.caption("Note: Each cell represents the RGB value of a pixel in the image.")
