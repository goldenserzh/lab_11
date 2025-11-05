

# main.py
from fastapi import FastAPI, HTTPException, Depends
from typing import List
import uvicorn
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Book as DBBook
from schemas import Book, BookCreate

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books", response_model=List[Book], 
         tags=['Книги'], 
         summary='Получение всех книг')
def get_all_books(db: Session = Depends(get_db)):
    return db.query(DBBook).all()

@app.get("/books/{book_id}", 
         response_model=Book, 
         tags=['Книги'], 
         summary="Получение одной книги")
def get_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book = db.query(DBBook).filter(DBBook.id == book_id).first()
    except:
        raise HTTPException(status_code=404, detail="Книга не была найдена")
    return book

@app.post("/books", 
          response_model=Book,
          tags=['Книги'],
          summary='Добавление книги')
def post_book(newbook: BookCreate, db: Session = Depends(get_db)):

    db_book = DBBook(title=newbook.title, author=newbook.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/books/{book_id}", 
         response_model=Book,
         tags=['Книги'],
         summary='Изменение информации о книге')
def update_book(book_id: int, update_data: BookCreate, db: Session = Depends(get_db)):
    try:
        book = db.query(DBBook).filter(DBBook.id == book_id).first()
        book.title = update_data.title
        book.author = update_data.author
        db.commit()
        db.refresh(book)
    except:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@app.delete("/books/{book_id}",
            tags = ['Книги'],
            summary='Удаление книги из бд')
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book = db.query(DBBook).filter(DBBook.id == book_id).first()
        db.delete(book)
        db.commit()
    except:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"detail": "Книга успешно удалена"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)