from pandas import DataFrame
from PIL import Image
import streamlit as st

st.set_page_config("img2rgb", "🌈")

st.title("🌈 Image to RGB")

uploaded_image = st.file_uploader("Upload an image", ["jpg", "jpeg", "png", "webp"])

if uploaded_image is not None:
    _, centered_column, _ = st.columns(3)
    centered_column.image(uploaded_image, width=200)

    image = Image.open(uploaded_image).convert("RGB")

    image_attrs = {
        "Filename": uploaded_image.name,
        "Type": uploaded_image.type,
        "Mode": image.mode,
        "Resolution": f"{image.width} × {image.height}",
    }

    st.table(image_attrs)

    with st.spinner("Getting RGB value for each pixel..."):
        pixel_rgbs = [
            [image.getpixel((x, y)) for x in range(image.width)]
            for y in range(image.height)
        ]

    with st.spinner("Converting pixel data to DataFrame..."):
        df = DataFrame(pixel_rgbs)
        df.index += 1
        df.columns += 1
        df.index.name = "Px"

    with st.spinner("Displaying result..."):
        st.dataframe(df)
        st.caption("Note: Each cell represents the RGB value of a pixel in the image.")
