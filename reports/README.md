
# 🧠 AI-Powered Product Label Scanner

This project is an intelligent food product label scanner built using **OCR (Optical Character Recognition)** and **Barcode decoding** to extract and retrieve detailed product information via the **Open Food Facts API**.

---

## 🚀 Features

- 📷 Upload product label images via interactive **Streamlit UI**
- 🔍 Extract text using **OCR (OpenCV + easyocr)**
- 🧾 Highlight detected text directly on the image
- 📦 Identify product name and retrieve details:
  - Product name, brand
  - Ingredients, categories
  - Nutrition facts (carbohydrates, fats, proteins, etc.)
- 📇 Detect and decode **Barcodes (EAN/UPC)** using `pyzbar`
- 🌐 Fetch accurate product details using **Open Food Facts API**
- 📊 Match and rank top related products from OCR text
- ✅ Handles noisy images, blurry text, and multilingual labels

---

## 🧰 Tech Stack

| Component           | Tools Used                         |
|---------------------|------------------------------------|
| OCR Engine          | EasyOCR, OpenCV                    |
| Barcode Reader      | Pyzbar                             |
| Backend Framework   | Python, Streamlit                  |
| API Integration     | Open Food Facts API                |
| UI/UX               | Streamlit with interactive widgets |
| Deployment Ready    | Streamlit                          |

---

## 🛠️ Installation

> ⚠️ Recommended: Use a virtual environment (e.g. `venv`, `conda`)

```bash
git clone https://github.com/your-username/product-label-scanner.git
cd product-label-scanner

# Create and activate environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
