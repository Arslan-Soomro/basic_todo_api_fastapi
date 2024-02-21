from . import models, schemas, crud
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, Request, Response

models.Base.metadata.create_all(bind=engine)

app = FastAPI();


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
def read_root() -> dict:
    return {"Hello": "World"};


# Create a new todo
@app.post("/todos/", tags=["Todos"], response_model=schemas.Todo)
def create_todo(todo: schemas.TodoBase, db: Session = Depends(get_db)) -> schemas.Todo:
    return crud.create_todo(db, todo)

@app.get("/todos/", tags=["Todos"], response_model=list[schemas.Todo])
def read_todos(db: Session = Depends(get_db)) -> list[schemas.Todo]:
    return crud.get_todos(db)

@app.get("/todos/{todo_id}", tags=["Todos"], response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)) -> schemas.Todo | HTTPException:
    db_todo = crud.get_todo(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo