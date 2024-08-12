from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    Captcha,
    DecodedCaptchaResponse,
)
from .utils.captcha import (
    convert_base64_to_binary,
    decode_captcha_from_binary,
)


app = FastAPI(
    title="TMS Captcha Solver API",
    description="This API is used to solve the captcha from the base64 image.",
    version="0.0.1",
    redoc_url=None,
    docs_url="/docs",
    openapi_url="/openapi.json",
    contact={
        "name": "Arjun Adhikari",
        "url": "https://linkedin.com/in/thearjun",
        "email": "mailarjunadhikari@gmail.com",
    },
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/", response_model=DecodedCaptchaResponse)
async def decode_captcha(captcha: Captcha):
    binary_captcha = convert_base64_to_binary(captcha.base64Image)
    captcha_text = await decode_captcha_from_binary(binary_captcha)
    return {"result": captcha_text}
