import matplotlib.pyplot as plt
from pandas import DataFrame
from PIL import Image
import streamlit as st

import colorsys

st.set_page_config(
    page_title="imgproc", 
    page_icon="🖼️"
)

st.title("🖼️Image Processing 🖼️")

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
        pixel_hsls = [
            [tuple(round(val, 2) for val in colorsys.rgb_to_hls(r / 255, g / 255, b / 255)) for r, g, b in row]
            for row in pixel_rgbs
        ]

    with st.spinner("Converting pixel data to DataFrame..."):
        df = DataFrame(pixel_rgbs)
        df.index += 1
        df.columns += 1
        df.index.name = "Px"

    with st.spinner("Displaying pixel data..."):
        st.subheader("Pixel Data")
        st.dataframe(df)
        st.caption("Note: Each cell represents the RGB value of a pixel in the image.")

    st.divider()

    n_channels = 7
    n_colors = 256

    with st.spinner("Calculating pixel frequency..."):
        px_freq = [[0 for _ in range(n_colors)] for _ in range(n_channels)]
        for y in pixel_rgbs:
            for rgb in y:
                grayscale = round(sum(rgb) / 3)
                for c in range(3):
                    px_freq[c][rgb[c]] += 1
                px_freq[3][grayscale] += 1
        for row in pixel_hsls:
            for hsl in row:
                hue_bin, saturation_bin, lightness_bin = [int(val * 255) for val in hsl]
                px_freq[4][hue_bin] += 1
                px_freq[5][saturation_bin] += 1
                px_freq[6][lightness_bin] += 1

    with st.spinner("Displaying pixel frequency data..."):
        df = DataFrame(
            px_freq, 
            index=["R", "G", "B", "GS", "Hue", "Saturation", "Lightness"]
        )
        st.subheader("Pixel Frequency Data")
        st.dataframe(df)
        st.divider()

    with st.spinner("Creating RGB and Grayscale histograms..."):
        fig, ax = plt.subplots(2, 2, figsize=(12, 12))
        rgbg_labels = ["Red", "Green", "Blue", "Gray"]
        for c in range(4):
            row, col = divmod(c, 2)
            ax[row, col].bar(
                range(n_colors), px_freq[c], label=rgbg_labels[c], color=rgbg_labels[c].lower()
            )
            ax[row, col].set_title(rgbg_labels[c])
            ax[row, col].set_xlabel("Pixel Intensity")

        plt.tight_layout()

        st.subheader("RGB and Grayscale Histograms")
        st.pyplot(fig)
        st.divider()

    with st.spinner("Creating HSL Histogram..."):
        fig_hsl, ax_hsl = plt.subplots(3, 1, figsize=(6, 12))
        hsl_labels = ["Hue", "Saturation", "Lightness"]
        color_hsl = ["brown", "pink", "violet"]
        for c in range(3):
            ax_hsl[c].bar(range(n_colors), px_freq[c + 4], label=hsl_labels[c], color=color_hsl[c])
            ax_hsl[c].set_title(hsl_labels[c])
            ax_hsl[c].set_xlabel("Pixel Intensity")
        plt.tight_layout()
        st.subheader("HSL Histograms")
        st.pyplot(fig_hsl)
        st.divider()

    with st.spinner("Normalizing histograms..."):
        total_pixels = image.width * image.height
        for i in range(n_channels):
            for j in range(n_colors):
                px_freq[i][j] /= total_pixels

    with st.spinner("Displaying normalized pixel frequency data..."):
        df = DataFrame(px_freq, index=["R", "G", "B", "GS"])
        st.subheader("Normalized Pixel Frequency Data")
        st.dataframe(df)

    with st.spinner("Creating normalized RGB and Grayscale histograms..."):
        fig, ax = plt.subplots(2, 2, figsize=(10, 8))
        for c in range(n_channels):
            row, col = divmod(c, 2)
            ax[row, col].bar(
                range(n_colors), px_freq[c], label=labels[c], color=labels[c]
            )
            ax[row, col].set_title(labels[c])
            ax[row, col].set_xlabel("Pixel Intensity")
            ax[row, col].set_ylabel("Pixel Frequency")
        plt.suptitle("Normalized Histograms")
        plt.tight_layout()

        st.subheader("Normalized Histograms")
        st.pyplot(fig)
