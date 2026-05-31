from fastapi import APIRouter, HTTPException, status
from FastAPI.db.models.User import User
from FastAPI.db.client import db_client
from FastAPI.db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(tags=["users_db"], prefix="/usersdb")

    
users_list = []

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}")
async def users(id: str):
    
    return search_user("_id", ObjectId(id))
    
@router.get("/")
async def userquery(id: str):
    return search_user("_id", ObjectId(id))

@router.post("/", status_code=201, response_model=User)
async def create_user(user: User):
    
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
   
    user_dict = dict(user)
    del user_dict["id"]
        
    id = db_client.users.insert_one(user_dict).inserted_id
    
    new_user = user_schema(db_client.users.find_one({"_id": id})) 
    
    
    return User(**new_user)

@router.put("/", response_model=User)
async def update_user(user: User): 
    
    try: 
        user_dict = dict(user)
        del user_dict["id"]
        
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha encontrado el usuario"} 
    
    return search_user("_id", ObjectId(user.id))
        

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str): 
    found = db_client.users.find_one_and_delete({"_id" : ObjectId(id)})
        
    if not found:
        return {"error": "No se ha encontrado el usuario"} 

    
    
def search_user(field:str , key):
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        return User(**user)
    except:
        return {"error": "No se ha encontrado el usuario"}