import string
from io import BytesIO
import base64
import cv2
import numpy as np
import pytesseract
from PIL import Image
from w3lib.html import replace_escape_chars

def convert_base64_to_binary(base64_string):
    base64_bytes = base64_string.encode("ascii")
    return base64.b64decode(base64_bytes)



async def decode_captcha_from_binary(response_binary):
    captcha_image = Image.open(BytesIO(response_binary))
    captcha_image = captcha_image.crop((80, 20, 210, 60))
    # convert PIL image to OpenCV image
    captcha_cv_image = cv2.cvtColor(np.array(captcha_image), cv2.COLOR_RGB2BGR)
    # remove background noise using thresholding
    # remove salt and pepper noise using median filter
    captcha_cv_image = cv2.medianBlur(captcha_cv_image, 3)
    # remove background noise using thresholding
    captcha_gray_image = cv2.cvtColor(captcha_cv_image, cv2.COLOR_BGR2GRAY)
    _, captcha_thresh = cv2.threshold(captcha_gray_image, 0, 255, cv2.THRESH_OTSU)
    # convert OpenCV image back to PIL image
    captcha_pil_image = Image.fromarray(captcha_thresh)
    # process captcha image using Tesseract OCR
    captcha_text = pytesseract.image_to_string(captcha_pil_image)
    # Replace special characters
    for char in string.punctuation:
        if char in captcha_text:
            captcha_text = captcha_text.replace(char, "")
    # Remove HTML tags
    captcha_text = replace_escape_chars(captcha_text)
    # Remove spaces
    captcha_text = captcha_text.replace(" ", "")
    return captcha_text
