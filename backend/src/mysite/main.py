from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field
import uvicorn
from uuid import UUID , uuid4
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_CONECTION_STRING = os.environ["MONGODB_CONNECTION_STRING"]
client = AsyncIOMotorClient(MONGODB_CONECTION_STRING , uuidRepresentation="standard")
db = client.todolist
todos = db.todos
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoItem(BaseModel):
    id : UUID = Field(default_factory=uuid4 , alias="_id") 
    title : str

class TodoItemCreate(BaseModel):
    title : str

# todos : list[TodoItem] = []
# id_counter = 1

@app.post("/todos" , response_model=TodoItem)
async def create_todo(todo_item : TodoItemCreate):
    try:
        global id_counter 
        new_todo = TodoItem(title=todo_item.title)
        # todos.append(new_todo)
        await todos.insert_one(new_todo.model_dump(by_alias=True))
        return new_todo
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400 , detail=str(e))
    

@app.get("/todos" , response_model=list[TodoItem])
async def read_todos():
    try:
        return await todos.find().to_list(length=None)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400 , detail=str(e))

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id : UUID):
    delete_result = await todos.delete_one({"_id" : todo_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404 , detail="Item not found")
    # for i , todo in enumerate(todos):
        # if todo.id == todo_id:
        #     todos.pop(i)
        #     return {"message" : "Todo item deleted successfully"}
    return {"message" : "Todo item deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app , host="0.0.0.0" , port=8000)