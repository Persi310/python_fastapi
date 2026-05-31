from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/products", responses={404: {"message": "No encontrado"}}, tags=["products"])

class Product(BaseModel):
    id : int
    name: str
    presentation: str


products_list = [Product(id = 1, name = "John", presentation = "Doe"),
         Product(id = 2, name = "John", presentation = "Doe"),
         Product(id = 3, name = "John", presentation = "Doe"),]

@router.get("")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return search_product(id)





def search_product(id: int):
    products = filter(lambda product: product.id == id, products_list)
    try:
        return list(products)[0]
    except:
        return {"error": "No se ha encontrado el producto"}
    