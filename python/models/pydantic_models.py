from pydantic import BaseModel


class FaceInfoIn(BaseModel):
    uid: str
    name: str
    image: str
