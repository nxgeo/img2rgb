import streamlit as st
from stegano import lsb
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Image Steganography", 
    page_icon="⌨",
    layout="wide"
)

def encode_message(image, message):
    encoded_image = lsb.hide(image, message.encode())
    return encoded_image

def decode_message(image):
    decoded_message = lsb.reveal(image)
    return decoded_message

st.title("Image Steganography")
# Radio button for selecting action (Encode/Decode)
selected_action = st.radio("Select Action", ["Encode", "Decode"])

# Display file uploader based on the selected action
if selected_action == "Encode":
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg", "webp"])
    if uploaded_image:
        # Create three columns layout
        col1, col2, col3 = st.columns(3)

        # Column 1: Preview Image and Binary Pixel Data Table
        pil_image = Image.open(uploaded_image)
        col1.image(pil_image, caption="Uploaded Image", use_column_width=True)

        # Column 2: Text Area for Message Input and Encode Button
        message = col2.text_area("Enter Message")
        if col2.button("Encode Message"):
            try:
                if message:
                    # Encode the message into the image
                    encoded_image = encode_message(pil_image, message)

                    # Display steganographic image
                    col3.image(encoded_image, caption="Steganographic Image", use_column_width=True)

                    # Save the encoded image for download
                    with BytesIO() as output_buffer:
                        encoded_image.save(output_buffer, format="PNG")
                        col3.download_button("Download Steganographic Image", output_buffer.getvalue(), file_name="steganographic_image.png", key="download_button")
                else:
                    col3.warning("Please enter a message to encode.")
            except Exception as e:
                col3.error(f"Error: {e}")

elif selected_action == "Decode":
    uploaded_encoded_image = st.file_uploader("Upload Encoded Image", type=["jpg", "png", "jpeg", "webp"])
    if uploaded_encoded_image:
        # Create two columns layout
        col1, col2 = st.columns(2)

        # Column 1: Preview Encoded Image
        pil_encoded_image = Image.open(uploaded_encoded_image)
        col1.image(pil_encoded_image, caption="Uploaded Encoded Image", use_column_width=True)

        # Column 2: Decode Button and Decoded Message
        if col2.button("Decode Message"):
            try:
                # Decode the message from the encoded image
                decoded_message = decode_message(pil_encoded_image)
                col2.subheader("Decoded Message")
                col2.text_area("Decoded Message", decoded_message, disabled=True)
            except Exception as e:
                col2.error(f"Error: {e}")
