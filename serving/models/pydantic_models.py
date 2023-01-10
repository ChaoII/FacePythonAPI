from pydantic import BaseModel
from typing import  List


class FaceInfoIn(BaseModel):
    uid: str
    name: str
    images: List[str]
