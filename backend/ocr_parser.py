import easyocr
import re
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'])

def extract_text(image):
    """Extracts text from an image using EasyOCR (supports English)."""
    if isinstance(image, Image.Image):
        image = np.array(image)
    result = reader.readtext(image, detail=0)
    return "\n".join(result)

def extract_vendor(text):
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            return line.strip()
    return "Unknown"

def extract_amount(text):
    matches = re.findall(r"\d+[.,]\d{2}", text)
    amounts = [float(m.replace(",", ".")) for m in matches if float(m.replace(",", ".")) < 100000]
    return max(amounts) if amounts else 0.0

def extract_date(text):
    patterns = [
        r"\d{2}[/-]\d{2}[/-]\d{4}",  
        r"\d{4}[/-]\d{2}[/-]\d{2}",  
        r"\d{2}[/-]\d{2}[/-]\d{2}",  
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return "Unknown"
