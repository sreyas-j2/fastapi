from fastapi import APIRouter,Depends
from ..schemas import recognising
from ..utils import get_encoding,get_con,recognise
from pathlib import Path,PureWindowsPath

DIR=Path(__file__).resolve().parent.parent

router=APIRouter(prefix="/recognise",tags=["recognise"])

@router.post('/')
def input(form_data:recognising=Depends()):
    with open(Path(DIR,'uploads/image.jpg'),"wb") as file:
        info=form_data.file.file.read()
        file.write(info)
    encoding=get_encoding(Path(DIR,'uploads/image.jpg'))
    conn,cur=get_con()
    cur.execute("""SELECT id,face_encoding FROM users """)
    data=cur.fetchall()
    data = [dict(row) for row in data]
    index=recognise([i["face_encoding"] for i in data],encoding)
    print(index)
    user=data[index]["id"]
    conn,cur=get_con()
    cur.execute("""SELECT id, name, email FROM users where id=%s""",(user,))
    data=cur.fetchall()
    return {"message":data}