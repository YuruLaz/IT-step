from fastapi import FastAPI

app = FastAPI()


@app.get("/products")
def get_products():
    return {"message": "პროდუქტების სია წარმატებით მოიძებნა"}


@app.post("/products")
def create_product():
    return {"message": "პროდუქტი შეიქმნა წარმატებით"}


@app.put("/products")
def replace_product():
    return {"message": "პროდუქტი განახლდა წარმატებით"}


@app.patch("/products")
def update_product():
    return {"message": "პროდუქტი ნაწილობრივ განახლდა წარმატებით"}


@app.delete("/products")
def delete_product():
    return {"message": "პროდუქტი წაიშალა წარმატებით"}
