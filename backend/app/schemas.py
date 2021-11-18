from pydantic import BaseModel


class MaskedImage(BaseModel):
    msg: str
    rawImage: bytes
