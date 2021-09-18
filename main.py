from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10, q: Optional[List[str]] = Query(None)):
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=1, lt=1000),
    q: Optional[str] = Query(..., min_length=3, max_length=50, regex="^qParam", alias="item-query"),
    size: float = Query(..., gt=0, lt=10.5),
    short: bool = False
):
    item = {"item_id": item_id, size: size}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description!"})
    return item

@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    item_dict = item.dict()
    item_dict.update({"item_id": item_id})
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    if q:
        item_dict.update({"q": q})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., title="The ID of the item to update", ge=0, le=1000),
    item: Optional[Item] = None,
    user: Optional[User] = None,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {"item_id": item_id, "importance": importance}
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    if q:
        results.update({"q": q})
    return results

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None):
    item = {"user_id": user_id, "item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
