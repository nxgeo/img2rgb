import streamlit as st

# Create three columns
col1, col2, col3 = st.columns(3)

# User data for the three profiles (image URL and name)
url_image = "https://preview.redd.it/leaks-kafkas-light-cone-v0-j1xyw44bp12b1.png?width=1410&format=png&auto=webp&s=3c61dbe07fba67940a17b3ce6928fa6340ad3610"
profile1 = {"image_url": url_image, "name": "Arief"}
profile2 = {"image_url": url_image, "name": "Gina"}
profile3 = {"image_url": url_image, "name": "Niko"}

# Add photo profile and name to each column
col1.image(profile1["image_url"], caption=profile1["name"], use_column_width=True)
col1.write(profile1["name"])

col2.image(profile2["image_url"], caption=profile2["name"], use_column_width=True)
col2.write(profile2["name"])

col3.image(profile3["image_url"], caption=profile3["name"], use_column_width=True)
col3.write(profile3["name"])