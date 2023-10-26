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

    custom_css = """
        <style>
            thead {
                display: none;
            }
        </style>
    """

    # Display the custom CSS and the table
    st.markdown(custom_css, unsafe_allow_html=True)

    st.table(image_attrs)

    with st.spinner("Getting RGB value for each pixel..."):
        pixel_rgbs = [
            [image.getpixel((x, y)) for x in range(image.width)]
            for y in range(image.height)
        ]
        # Decimal Format
        pixel_hsls = [
            [tuple(round(val, 2) for val in colorsys.rgb_to_hls(r / 255, g / 255, b / 255)) for r, g, b in row]
            for row in pixel_rgbs
        ]
        # 255 Format
        pixel_hsl = [
            [tuple(int(val * 255) for val in hsl) for hsl in row]
            for row in pixel_hsls
        ]
        # Percentile Format
        pixel_hsls_percentile = [
            [(int(round(hsl[0] * 100)), int(round(hsl[1] * 100)), int(round(hsl[2] * 100))) for hsl in row]
            for row in pixel_hsls
        ]

    with st.spinner("Converting RGB pixel data to DataFrame..."):
        df_rgb = DataFrame(pixel_rgbs)
        df_rgb.index += 1
        df_rgb.columns += 1
        df_rgb.index.name = "Px"

    with st.spinner("Converting HSL pixel data decimal to DataFrame..."):
        df_hsls = DataFrame(pixel_hsls_percentile)
        df_hsls.index += 1
        df_hsls.columns += 1
        df_hsls.index.name = "Px"

    with st.spinner("Converting HSL pixel data 255 format to DataFrame..."):
        df_hsl = DataFrame(pixel_hsl)
        df_hsl.index += 1
        df_hsl.columns += 1
        df_hsl.index.name = "Px"

    with st.spinner("Displaying RGB pixel data..."):
        st.subheader("RGB Pixel Data Table")
        st.dataframe(df_rgb)
        st.caption("Note: Each cell represents the RGB value of a pixel in the image.")

    st.divider()

    with st.spinner("Displaying HSL pixel data..."):
        st.subheader("HSL Pixel Data Table (percentile format)")
        st.dataframe(df_hsls)
        st.caption("Note: Each cell represents the HSL value of a pixel in the image.")

    st.divider()

    with st.spinner("Displaying HSL pixel data..."):
        st.subheader("HSL Pixel Data Table (255 Format)")
        st.dataframe(df_hsl)
        st.caption("Note: Each cell represents the HSL value of a pixel in the image.")

    n_channels = 7
    n_colors = 256
    labels = ["Red", "Green", "Blue", "Gray", "Hue", "Saturation", "Lightness"]

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
        fig_hsl, ax_hsl = plt.subplots(1, 3, figsize=(10, 4))
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
        # Calculate total number of pixels
        total_pixels = image.width * image.height

        # Normalize histograms
        normalized_px_freq = [[freq / total_pixels for freq in channel] for channel in px_freq]
        normalized_hue_freq = [freq / total_pixels for freq in px_freq[4]]
        normalized_saturation_freq = [freq / total_pixels for freq in px_freq[5]]
        normalized_lightness_freq = [freq / total_pixels for freq in px_freq[6]]

        # Display normalized pixel frequency data
    with st.spinner("Displaying normalized pixel frequency data..."):
        df_normalized = DataFrame(
            normalized_px_freq, 
            index=["R", "G", "B", "GS", "Hue", "Saturation", "Lightness"]
        )
        st.subheader("Normalized Pixel Frequency Data")
        st.dataframe(df_normalized)

    # Creating normalized RGB and Grayscale histograms
    with st.spinner("Creating normalized RGB and Grayscale histograms..."):
        fig_normalized, ax_normalized = plt.subplots(2, 2, figsize=(10, 8))
        for c in range(n_channels):
            row, col = divmod(c, 2)
            if row < 2 and col < 2:
                ax_normalized[row, col].bar(
                    range(n_colors), normalized_px_freq[c], label=labels[c], color=labels[c]
                )
                ax_normalized[row, col].set_title(labels[c])
                ax_normalized[row, col].set_xlabel("Pixel Intensity")
        plt.suptitle("Normalized Histograms")
        plt.tight_layout()

        st.subheader("Normalized Histograms")
        st.pyplot(fig_normalized)

    # Create normalized HSL histograms
    with st.spinner("Creating normalized HSL histograms..."):
        fig_normalized_hsl, ax_normalized_hsl = plt.subplots(1, 3, figsize=(10, 4))
        hsl_labels = ["Hue", "Saturation", "Lightness"]
        normalized_hsl_freq = [normalized_hue_freq, normalized_saturation_freq, normalized_lightness_freq]
        color_hsl = ["brown", "pink", "violet"]
        for c in range(3):
            ax_normalized_hsl[c].bar(range(n_colors), normalized_hsl_freq[c], label=hsl_labels[c], color=color_hsl[c])
            ax_normalized_hsl[c].set_title(hsl_labels[c])
            ax_normalized_hsl[c].set_xlabel("Pixel Intensity")
        plt.tight_layout()
        st.subheader("Normalized HSL Histograms")
        st.pyplot(fig_normalized_hsl)