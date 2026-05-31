from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

class User(BaseModel):
    id : int
    name: str
    surname: str
    url: str
    age: int
    
users_list = [User(id = 1, name = "John", surname = "Doe", url = "https://mouredev.com", age = 30),
         User(id = 2, name = "John", surname = "Doe", url = "https://mouredev.com", age = 30),
         User(id = 3, name = "John", surname = "Doe", url = "https://mouredev.com", age = 30),]

@router.get("/users")
async def users():
    return users_list

@router.get("/users/{id}")
async def users(id: int):
    return search_user(id)
    
@router.get("/userquery")
async def userquery(id: int):
    return search_user(id)

@router.post("/user", status_code=201)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else:
        users_list.append(user)
        return {"message": "Usuario creado correctamente"}

@router.put("/user")
async def update_user(user: User): 
    
    found = False 
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            return {"message": "Usuario actualizado correctamente"}
        
    if not found:
        return {"error": "No se ha encontrado el usuario"} 

@router.delete("/user/{id}")
async def delete_user(id: int): 
    found = False 
    
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"message": "Usuario eliminado correctamente"}
        
    if not found:
        return {"error": "No se ha encontrado el usuario"} 

    
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
    
    
    
    
@router.get("/users")
async def usersjson():
    return [{"name": "John Doe", "surname": "moure", "url": "https://mouredev.com", "age": 30}, 
            {"name": "John Doe", "surname": "moure", "url": "https://mouredev.com", "age": 30}, 
            {"name": "John Doe", "surname": "moure", "url": "https://mouredev.com", "age": 30},]