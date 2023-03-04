from pydantic import BaseModel
from typing import Optional
from fastapi import Form,File,UploadFile
from dataclasses import dataclass


class user(BaseModel):
    name: str
    email: str
    info: Optional[str]=None


@dataclass
class SimpleModel:
    name: str= Form(...)
    email: str= Form(...)
    # info: Optional[str]=Form(...)
    info: UploadFile=File(...)

@dataclass
class recognising:
    file: UploadFile=File(...)