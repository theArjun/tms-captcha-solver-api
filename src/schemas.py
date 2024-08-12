from pydantic import BaseModel


class Captcha(BaseModel):
    base64Image: str


class DecodedCaptchaResponse(BaseModel):
    result: str
