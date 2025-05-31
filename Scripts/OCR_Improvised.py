import streamlit as st
import re
import requests
import easyocr
import cv2
import numpy as np
from PIL import Image
import tempfile

# ------------------- Web UI -------------------
st.set_page_config(page_title="OCR Product Finder", layout="wide")
st.markdown("""
    <h1 style="
        text-align: center;
        background: linear-gradient(to right, #FF512F, #DD2476);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Segoe UI', sans-serif;
        font-size: 3em;
        margin-bottom: 0.5em;
    ">
        🧾 OCR/Barcode Based Product Info Finder(IMPROVISED MODEL)
    </h1>
""", unsafe_allow_html=True)


st.markdown('<div class="subtitle">Upload an image of a food product label to retrieve its information.</div>', unsafe_allow_html=True)



# Upload image
uploaded_image = st.file_uploader("📤 Upload Product Image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_image:
    # Display image
    #st.image(uploaded_image, caption="Uploaded Image")

    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_image.read())
    temp_file_path = temp_file.name

    # OCR
    st.spinner("Running OCR using EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(temp_file_path)

    # Draw results using OpenCV
    image_np = cv2.imread(temp_file_path)
    for (bbox, text, prob) in results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image_np, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    st.image(image_np, caption="Detected Text", channels="BGR")

    # Extract text
    v_list = [results[i][1] for i in range(len(results))]
    cleaned_list = [re.sub(r'[^A-Za-z0-9]', '', val) for val in v_list if val.strip()]
    combined = ' '.join(cleaned_list)

    st.success("Extracted & Cleaned Text:")
    st.code(combined, language='text')

    # Search Open Food Facts API
    def search_open_food_facts(query, max_products=3):
        api_url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={query}&search_simple=1&json=1"
        response = requests.get(api_url)
        try:
            data = response.json()
        except ValueError:
            return []
        return data.get('products', [])[:max_products]

    st.markdown("---")
    st.subheader("🔍 Product Search Results")
    with st.spinner('Searching for Match'):
     for word in cleaned_list:
        st.markdown(f"### Keyword: `{word}`")
        result_re = search_open_food_facts(word)

        if result_re:
            for i, product in enumerate(result_re):
                st.markdown(f"**Product {i+1}:**")
                st.markdown(f"- **Name:** {product.get('product_name', 'N/A')}")
                st.markdown(f"- **Brand:** {product.get('brands', 'N/A')}")
                st.markdown(f"- **Categories:** {product.get('categories', 'N/A')}")
                st.markdown(f"- **Ingredients:** {product.get('ingredients_text', 'N/A')}")
                st.markdown(f"- **Nutrition Facts:** {product.get('nutriments', {})}")
                st.markdown("---")
        else:
            st.warning("No relevant products found.")
