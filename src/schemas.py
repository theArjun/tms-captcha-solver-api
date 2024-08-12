from pydantic import BaseModel


class Captcha(BaseModel):
    base64Image: str
