from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator

app = FastAPI()


class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0)
    discount_price: float | None = None
    quantity: int = Field(..., ge=0)
    category: str
    sku: str = Field(..., min_length=5, max_length=20)
    email: EmailStr
    stock: bool = True

    @field_validator("name")
    @classmethod
    def clean_name(cls, v: str) -> str:
        return v.strip()

    @field_validator("sku")
    @classmethod
    def clean_sku(cls, v: str) -> str:
        if " " in v:
            raise ValueError("sku cannot contain spaces")
        return v.upper()

    @model_validator(mode="after")
    def check_discount(self):
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("discount_price must be less than price")
        return self


class ProductResponse(BaseModel):
    name: str
    price: float
    discount_price: float | None = None
    quantity: int
    category: str
    stock: bool


products: list[Product] = []


@app.post("/products", response_model=ProductResponse)
def create_product(product: Product):
    products.append(product)
    return product


@app.get("/products", response_model=list[ProductResponse])
def get_products():
    return products
