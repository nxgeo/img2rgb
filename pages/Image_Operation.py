import streamlit as st
from PIL import Image, ImageChops
import numpy as np
from pandas import DataFrame

st.set_page_config(
    page_title="Image Operation", 
    page_icon="🖼️",
    layout="wide"
)

custom_css = """
        <style>
            thead {
                display: none;
            }
        </style>
    """

st.title("🖼️Image Operation")

# Set up the layout with two columns
col1, col2 = st.columns(2)

# In the first column, allow users to upload images
uploaded_file_col1 = col1.file_uploader("Upload Image for Column 1", type=["jpg", "png", "jpeg", "webp"])

# In the second column, allow users to upload images
uploaded_file_col2 = col2.file_uploader("Upload Image for Column 2", type=["jpg", "png", "jpeg", "webp"])

result_image = None

# Display the uploaded images in respective columns
if uploaded_file_col1 is not None:
    image_col1 = Image.open(uploaded_file_col1).convert("RGB")
    col1.image(image_col1, caption='Preview Image for Column 1.', width=200, use_column_width=False)

    image_attrs_col1 = {
        "Filename": uploaded_file_col1.name,
        "Type": uploaded_file_col1.type,
        "Mode": image_col1.mode,
        "Resolution": f"{image_col1.width} × {image_col1.height}",
    }

    # Display the custom CSS and the table
    st.markdown(custom_css, unsafe_allow_html=True)

    with col1:
        st.table(image_attrs_col1)

        with st.spinner("Getting Pixel value for each pixel in Column 1..."):
            pixel_data_col1 = [
                [image_col1.getpixel((x, y)) for x in range(image_col1.width)]
                for y in range(image_col1.height)
            ]
            df_rgb_col1 = DataFrame(pixel_data_col1)
            df_rgb_col1.index += 1
            df_rgb_col1.columns += 1
            df_rgb_col1.index.name = "Px"

            st.subheader("Pixel Data Table Column 1")
            st.dataframe(df_rgb_col1)
            st.caption("Note: Each cell represents the value of a pixel in the image.")


if uploaded_file_col2 is not None:
    image_col2 = Image.open(uploaded_file_col2).convert("RGB")
    col2.image(image_col2, caption='Preview Image for Column 2.', width=200, use_column_width=False)

    image_attrs_col2 = {
        "Filename": uploaded_file_col2.name,
        "Type": uploaded_file_col2.type,
        "Mode": image_col2.mode,
        "Resolution": f"{image_col2.width} × {image_col2.height}",
    }

    # Display the custom CSS and the table
    st.markdown(custom_css, unsafe_allow_html=True)

    with col2:
        st.table(image_attrs_col2)

        with st.spinner("Getting Pixel value for each pixel in Column 2..."):
            pixel_data_col2 = [
                [image_col2.getpixel((x, y)) for x in range(image_col2.width)]
                for y in range(image_col2.height)
            ]
            df_rgb_col2 = DataFrame(pixel_data_col2)
            df_rgb_col2.index += 1
            df_rgb_col2.columns += 1
            df_rgb_col2.index.name = "Px"

            st.subheader("Pixel Data Table Column 2")
            st.dataframe(df_rgb_col2)
            st.caption("Note: Each cell represents the value of a pixel in the image.")

# Dropdown
if uploaded_file_col1 is not None and uploaded_file_col2 is not None:
    image_col1 = image_col1.convert('1')
    image_col2 = image_col2.convert('1')
    selected_option = st.selectbox(
        "Select an option", 
        ["AND", "OR", "XOR", "NAND", "NOR", "XNOR", "+", "-", "*", "/"]
    )
    st.write("You selected:", selected_option)

    if selected_option == "AND":
        result_image = ImageChops.logical_and(image_col1, image_col2)
        st.image(result_image, caption="Result Image(Logical AND)", width=400, use_column_width=False)

    elif selected_option == "OR":
        result_image = ImageChops.logical_or(image_col1, image_col2)
        st.image(result_image, caption="Result Image(Logical OR)", width=400, use_column_width=False)
    
    elif selected_option == "XOR":
        result_image = ImageChops.logical_xor(image_col1, image_col2)
        st.image(result_image, caption="Result Image(Logical XOR)", width=400, use_column_width=False)

    elif selected_option == "NAND":
        and_result = ImageChops.logical_and(image_col1, image_col2)
        result_image = ImageChops.invert(and_result)
        st.image(result_image, caption='Result Image (Logical NAND)', width=400, use_column_width=False)

    elif selected_option == "NOR":
        or_result = ImageChops.logical_or(image_col1, image_col2)
        result_image = ImageChops.invert(or_result)
        st.image(result_image, caption='Result Image (Logical NOR)', width=400, use_column_width=False)

    elif selected_option == "XNOR":
        xor_result = ImageChops.logical_xor(image_col1, image_col2)
        result_image = ImageChops.invert(xor_result)
        st.image(result_image, caption='Result Image (Logical XNOR)', width=400, use_column_width=False)

    elif selected_option == "+":
        # Perform addition operation on images
        result_image = ImageChops.add(image_col1, image_col2)
        st.image(result_image, caption='Result Image (Addition)', width=400, use_column_width=False)

    elif selected_option == "-":
        # Perform subtraction operation on images
        result_image = ImageChops.subtract(image_col1, image_col2)
        st.image(result_image, caption='Result Image (Subtraction)', width=400, use_column_width=False)

    elif selected_option == "*":
        # Perform multiplication operation on images
        result_image = ImageChops.multiply(image_col1, image_col2)
        st.image(result_image, caption='Result Image (Multiplication)', width=400, use_column_width=False)
    
    elif selected_option == "/":
        # Convert images to NumPy arrays and ensure they are in float64 data type
        array1 = np.array(image_col1, dtype=np.float64)
        array2 = np.array(image_col2, dtype=np.float64)

        # Ensure non-zero values in array2 to avoid division by zero
        array2[array2 == 0] = 1

        # Perform division operation and clip values to [0, 255]
        result_array = np.clip(array1 / array2, 0, 255)

        # Convert the NumPy array back to an image with uint8 data type
        result_array = result_array.astype(np.uint8)
        result_image = Image.fromarray(result_array)
        st.image(result_image, caption='Result Image (Division)', width=400, use_column_width=False)

if result_image is not None:
    result_image = result_image.convert("RGB")
    width_result, height_result = result_image.size
    pixel_data_res = [
        [result_image.getpixel((x, y)) for x in range(width_result)] 
        for y in range(height_result)
    ]
    df_rgb_res = DataFrame(pixel_data_res)
    df_rgb_res.index += 1
    df_rgb_res.columns += 1
    df_rgb_res.index.name = "Px"
    st.subheader("Pixel Data Table Result Image")
    st.dataframe(df_rgb_res)
    st.caption("Note: Each cell represents the value of a pixel in the image.")