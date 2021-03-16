from fastapi import FastAPI
from enum import Enum

app = FastAPI()

# enum + enum route
class ModelName(str, Enum):
    messi = 'messi'
    jordan = 'jordan'

@app.get('/models/{model_name}')
async def get_models(model_name: ModelName):
    print(model_name, model_name.value)
    if model_name == ModelName.messi:
        return {model_name: f'we have {model_name}.'}

# default 
@app.get('/')
async def hello():
    return {'message': 'Hello World'}

# path param
@app.get('/item/{item_id}')
async def read_item(item_id: int):
    return {"item_id": item_id}

# query param (w/ Optional)
from typing import Optional
@app.get('/item/')
async def read_query(size: int = 77, length: int = 99, width: Optional[str] = None):
    return {'size': size, 'length': length, 'width': width}

# request body (w/ BaseModel from Pydantic)
from pydantic import BaseModel
class Item(BaseModel):
    name: str
    age: int
    address: Optional[int]
@app.post('/items/')
async def create_item(item: Item):
    print(item.age + item.age)
    return item
