from fastapi import FastAPI , HTTPException
from pydantic import BaseModel # it is used to validate the request body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoItem(BaseModel):
    id : int
    title : str

class TodoItemCreate(BaseModel):
    title : str

todos : list[TodoItem] = []
id_counter = 1

@app.post("/todos" , response_model=TodoItem)
async def create_todo(todo_item : TodoItemCreate):
    try:
        global id_counter 
        new_todo = TodoItem(id=id_counter , title=todo_item.title)
        todos.append(new_todo)
        id_counter += 1
        return new_todo
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400 , detail=str(e))
    

@app.get("/todos" , response_model=list[TodoItem])
async def read_todos():
    return todos

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id : int):
    for i , todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {"message" : "Todo item deleted successfully"}
    raise HTTPException(status_code=404 , detail="Item not found")