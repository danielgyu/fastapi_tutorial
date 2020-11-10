from enum     import Enum
from pydantic import BaseModel
from typing   import Optional
from fastapi  import FastAPI

class ModelName(str, Enum):
    alexnet = 'alexnet'
    resnet  = 'resnet'
    lenet   = 'lenet'

class Body(BaseModel):
    name        : str
    description : Optional[str] = None
    price       : float
    tax         : Optional[float] = None

fake_items_db = [{'item' : 'Foo', 'item' : 'Bar', 'item' : 'Baz'}]

app = FastAPI()


@app.get('/')
async def root():
    return {'message' : 'Hello from FastAPI'}

@app.get('/items/')
async def query_item(skip : int = 0, limit : int = 0):
    """receiving query string with default values"""
    return fake_items_db[skip : skip + limit]

@app.get('/items/{item_id}')
async def item(item_id : int):
    """receiving request argument"""
    return {'item_id' : item_id}

@app.get('/model/{models_id}')
async def optional_models(models_id : str, q : Optional[str] = None):
    """receiving argument AND an optional query string"""
    if q:
        return {'models_id' : models_id, 'q' : q}
    return {'models_id' : models_id}

@app.get('/models/{model_name}')
async def model(model_name : ModelName):
    """using pre-defined value in a response"""
    if model_name == ModelName.alexnet:
        return {'name': model_name, 'message' : 'ALEXNET'}
    if model_name.value == 'lenet':
        return {'name': model_name, 'message' : 'LENET'}
    return {'name': model_name, 'message' : 'RESIDUALS'}

@app.post('/body/')
async def body(body : Body):
    """receiving a request body based on type declaration above in class Body"""
    return body
