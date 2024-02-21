from sqlalchemy.orm import Session
from . import models, schemas

def get_todo(db: Session, todo_id: int):
    todo_data = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    return todo_data

def get_todos(db: Session):
    todos_data = db.query(models.Todo).all()
    return todos_data

def create_todo(db: Session, todo: schemas.TodoBase):
    todo_data = models.Todo(**todo.model_dump())
    db.add(todo_data)
    db.commit()
    db.refresh(todo_data)
    return todo_data


    
    