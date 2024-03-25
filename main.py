from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import Captcha
from utils.captcha import convert_base64_to_binary, decode_captcha_from_binary

CAPTCHA_LENGTH = 6

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/decode")
async def decode_captcha(captcha: Captcha):
    is_valid = True
    try:
        response_binary = convert_base64_to_binary(captcha.base64Image)
        captcha_text = await decode_captcha_from_binary(response_binary)
    except Exception:
        is_valid = False
        captcha_text = ""

    return {
        "is_valid": is_valid,
        "result": captcha_text,
    }
