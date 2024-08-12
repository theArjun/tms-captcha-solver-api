import base64
import string
from io import BytesIO

import cv2
import numpy as np
import pytesseract
from PIL import Image
from w3lib.html import replace_escape_chars


def convert_base64_to_binary(base64_string):
    """Convert a base64 encoded string to binary."""
    base64_bytes = base64_string.encode("ascii")
    return base64.b64decode(base64_bytes)


def preprocess_captcha_image(image):
    """Preprocess the captcha image by cropping, removing noise, and thresholding."""
    # Crop the image to focus on the captcha area
    cropped_image = image.crop((80, 20, 210, 60))
    # Convert PIL image to OpenCV image
    captcha_cv_image = cv2.cvtColor(np.array(cropped_image), cv2.COLOR_RGB2BGR)
    # Remove salt and pepper noise using median filter
    captcha_cv_image = cv2.medianBlur(captcha_cv_image, 3)
    # Convert to grayscale
    captcha_gray_image = cv2.cvtColor(captcha_cv_image, cv2.COLOR_BGR2GRAY)
    # Remove background noise using thresholding
    _, captcha_thresh = cv2.threshold(captcha_gray_image, 0, 255, cv2.THRESH_OTSU)
    # Convert OpenCV image back to PIL image
    return Image.fromarray(captcha_thresh)


def clean_captcha_text(text):
    """Clean the OCR extracted text by removing punctuation, HTML tags, and spaces."""
    # Remove special characters (punctuation)
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Remove HTML tags and escape characters
    text = replace_escape_chars(text)
    # Remove spaces
    return text.replace(" ", "")


async def decode_captcha_from_binary(response_binary):
    """Decode the captcha from binary response, preprocess it, and extract the text."""
    # Open the image from the binary response
    captcha_image = Image.open(BytesIO(response_binary))
    # Preprocess the image to enhance text recognition
    processed_image = preprocess_captcha_image(captcha_image)
    # Process captcha image using Tesseract OCR
    captcha_text = pytesseract.image_to_string(processed_image)
    # Clean the extracted text
    return clean_captcha_text(captcha_text)
