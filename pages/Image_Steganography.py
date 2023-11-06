import streamlit as st
from stegano import lsb
from PIL import Image
import numpy as np
from io import BytesIO
from pandas import DataFrame

st.set_page_config(
    page_title="Image Steganography", 
    page_icon="⌨",
    layout="wide"
)

def encode_message(image, message):
    encoded_image = lsb.hide(image, message.encode())
    return encoded_image

st.title("Image Steganography")
uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg", "webp"])

# Create three columns layout
col1, col2, col3 = st.columns(3)

# Column 1: Preview Image and Binary Pixel Data Table
if uploaded_image:
    pil_image = Image.open(uploaded_image)
    col1.image(pil_image, caption="Uploaded Image", use_column_width=True)

    # Convert image to binary pixel data
    binary_pixels = np.array(pil_image.convert("1"))  # Convert to 1-bit mode (binary)
    df_binary = DataFrame(binary_pixels)
    df_binary.index += 1
    df_binary.columns += 1
    df_binary.index.name = "Px"

    # Display binary pixel data table
    col1.subheader("Binary Pixel Data Table")
    col1.dataframe(df_binary)

    # Column 2: Text Area for Message Input
    message = col2.text_area("Enter Message to Encode")

    # Column 3: Display Encoded Image
    if col2.button("Encode Message"):
        if message:
            try:
                # Encode the message into the image
                encoded_image = encode_message(pil_image, message)

                # Display steganographic image
                col3.image(encoded_image, caption="Steganographic Image", use_column_width=True)

                # Save the encoded image for download
                with BytesIO() as output_buffer:
                    encoded_image.save(output_buffer, format="PNG")
                    col3.download_button("Download Steganographic Image", output_buffer.getvalue(), file_name="steganographic_image.png", key="download_button")
            except Exception as e:
                col3.error(f"Error: {e}")
        else:
            col3.warning("Please enter a message to encode.")
