from pydantic import BaseModel
from typing import Optional
from fastapi import Form,File,UploadFile
from dataclasses import dataclass


class user(BaseModel):
    name: str
    email: str
    info: Optional[str]=None

#using pydantic
# class userReg(BaseModel):
#     name: str
#     email: str
#     image: UploadFile
#     @classmethod
#     def convert_form(cls,name:str=Form(),email:str=Form(),image:UploadFile=File()):
#         return cls(name=name,email=email)

#using dataclass
@dataclass
class userReg:
    name: str=Form(...)
    email: str=Form(...)
    image: UploadFile=File(...)

@dataclass
class SimpleModel:
    name: str= Form(...)
    email: str= Form(...)
    info: UploadFile=File(...)

@dataclass
class recognising:
    file: UploadFile=File(...)