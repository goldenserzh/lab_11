from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uvicorn
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import User as DBUser
from schemas import User, CreateUser

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/users', 
         response_model=List[User],
         tags=['Пользователи'],
         summary='Получение информации о пользователях')
def get_users(db: Session=Depends(get_db)):
    return db.query(DBUser).all()
    
@app.get('/users/{user_id}',
         response_model=User,
         tags=['Пользователи'],
         summary='Получение информации о конкретном пользователе')
def get_user(user_id: int, db: Session=Depends(get_db)):
    try:
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
    except:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.post('/users',
          response_model=User,
          tags=['Пользователи'],
          summary='Добалвение пользователя')

def post_user(newuser: CreateUser, db: Session=Depends(get_db)):
    db_user = DBUser(name = newuser.name,
                     surname = newuser.surname,
                     age = newuser.age,
                     email = newuser.email)
    db.add(db_user)
    db.commit()
    return db_user


@app.put('/Users/{user_id}',
         response_model=User,
         tags = ['Пользователи'],
         summary='Изменения в информации о пользователе')

def change_info(user_id, update_data: CreateUser ,db: Session = Depends(get_db)):
    try:
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        user.name = update_data.name
        user.surname = update_data.surname
        user.age = update_data.age
        user.email = update_data.email
        db.commit()
        db.refresh()
    except:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return user


@app.delete('/users/{user_id}',
            tags = ['Пользователи'],
            summary='Изменения в информации о пользователе')

def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        db.delete(user)
        db.commit()
    except:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    
    return {"detail": "Пользователь удален"}

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, port=8080)