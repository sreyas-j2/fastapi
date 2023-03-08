from fastapi import HTTPException,APIRouter,status,Request,Depends,UploadFile,File,Form
from fastapi.responses import FileResponse
from ..schemas import user,SimpleModel,userReg
from random import randint
from fastapi.templating import Jinja2Templates
from pathlib import Path
from ..utils import get_con,get_encoding
import json

router=APIRouter(prefix="/users",tags=["users"])

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_PATH=Path(BASE_DIR,'uploads/image.jpg')
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@router.get('/')
def get_users(request: Request):
    conn,cur=get_con()
    cur.execute("""SELECT * FROM users """)
    data=cur.fetchall()
    return templates.TemplateResponse('item.html', {"request": request, "users": data})

#TODO:implement UI
@router.get('/{id}')
def get_user(id: int, request: Request):
    conn,cur=get_con()
    cur.execute("""SELECT * FROM users WHERE id=%s""",(id,))
    data=cur.fetchall()
    if not data:
        raise HTTPException(detail="user not found!",status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse('item.html', {"request": request, "users": data})

@router.post('/',status_code=status.HTTP_201_CREATED)
# def create_user(user_data:userReg= Depends(userReg.convert_form)):
def create_user(user_data:userReg=Depends()):
    with open(IMG_PATH,"wb") as file:
        info=user_data.image.file.read()
        file.write(info)
    encoding=get_encoding(IMG_PATH)
    conn,cur=get_con()
    ret=cur.execute("""INSERT INTO users (name,email,face_encoding) VALUES (%s,%s,%s)""",(user_data.name,user_data.email,list(encoding)))
    conn.commit()
    print(ret)
    return {"data":ret}#supposed to return the modified data

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    conn,cur=get_con()
    cur.execute("DELETE FROM users WHERE id=%s returning *",(id,))
    data=cur.fetchone()
    conn.commit()
    if not data:
        raise HTTPException(detail="user not found!",status_code=status.HTTP_404_NOT_FOUND)
    return {"data":data}

@router.put('/{id}')
def update_user(id:int, form_data:SimpleModel=Depends()):
    with open(IMG_PATH,"wb") as file:
        info=form_data.info.file.read()
        file.write(info)
    encoding=get_encoding(IMG_PATH)
    conn,cur=get_con()
    cur.execute("""UPDATE users SET name=%s, email=%s ,face_encoding=%s WHERE id=%s returning *""",(form_data.name,form_data.email,list(encoding),id))
    ret=cur.fetchone()
    conn.commit()
    if not ret:
        raise HTTPException(detail="user not found!",status_code=status.HTTP_404_NOT_FOUND)
    ret.pop("face_encoding")
    return {"data":ret}