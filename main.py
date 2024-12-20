from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#
app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "helloo"}
#
# @app.post("/")
# async def post():
#     return {"message": "helloo from post"}
#
# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     return {"user_id": user_id}
#
# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"
#
#
# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {"food_name": food_name, "message": "you are healthy"}
#
#     if food_name.value == "fruits":
#         return {
#             "food_name": food_name,
#             "message": "you are still healthy, but like sweet things",
#         }
#     return {"food_name": food_name, "message": "i like chocolate milk"}
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# @app.post("/items")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
#
# @app.put("/items/{item_id}")
# async def change_tem_name(item_id : int, item: Item):
#     if item_id:
#         item.name = 'name changed'
#     return item

# class User(BaseModel):
#     name: str
#     age: int
#
#
# class Item(BaseModel):
#     title: str
#     description: str
#
#
# @app.post("/create/")
# async def create_user_with_item(user: User, item: Item):
#     return {"user": user, "item": item}


# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "id": 1,
#                 "name": "John Doe",
#                 "age": 30
#             }
#         }
#
# @app.post("/create_user/")
# async def create_user(user: User):
#     return {"message": "User created successfully", "user": user}



# class User(BaseModel):
#     id: int
#     name: str
#     age: int
#
#
# @app.get("/users/{user_id}", response_model=User)
# def get_user(user_id: int):
#     user_data = {"id": user_id, "name": "John Doe", "age": 30}
#     return user_data


class User(BaseModel):
    id: int
    name: str
    age: int


users = []

@app.post("/users/")
def create_user(user: User):
    for existing_user in users:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
    users.append(user)
    return {"message": "User created successfully", "user": user}

@app.get("/users/")
def get_all_users():
    return {"users": users}

@app.get("/users/{name}")
def get_user(name: str):
    for user in users:
        if user.name == name:
            return {"user": user}
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return {"message": "User updated successfully", "user": updated_user}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            users.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
