import fastapi 
from fastapi import Depends 
from config import Session as SessionLocal,engine
import db_models
from models import Product
from sqlalchemy.orm import Session as DBSession


app=fastapi.FastAPI()  

@app.get("/")
def greet():
    return "Hello World"

db_models.Base.metadata.create_all(bind=engine)


products=[
    Product(id=1,name="phone",des="good phone",price=99, quantity=5),

    Product(id=2,name="laptop",des="good laptop",price=999, quantity=10),

]


def init_db():
    session=SessionLocal()
    count=session.query(db_models.Product).count()
    if count==0:
     product1=db_models.Product(name="phone",des="good phone",price=99, quantity=5)
     product2=db_models.Product(name="laptop",des="good laptop",price=999, quantity=10)
     session.add(product1)
     session.add(product2)
     session.commit()
init_db()


def get_db_session():
    session=SessionLocal()
    try:
        yield session
    finally:
        session.close()


     
@app.get("/products")
def get_all_products(db:DBSession=Depends(get_db_session)):
    return db.query(db_models.Product).all()




@app.get("/product/{id}")
def get_by_product_id(id:int, db:DBSession=Depends(get_db_session)):
    return db.query(db_models.Product).filter(db_models.Product.id == id).first()

@app.post("/product")
def create_products(product:Product, db:DBSession=Depends(get_db_session)): 
    new_product=db_models.Product(name=product.name, des=product.des, price=product.price, quantity=product.quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.put("/product/{id}")
def update_products(id:int, product:Product, db:DBSession=Depends(get_db_session)): 
    existing_product=db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if existing_product:
        existing_product.name=product.name
        existing_product.des=product.des
        existing_product.price=product.price
        existing_product.quantity=product.quantity
        db.commit()
        db.refresh(existing_product)
        return existing_product
    return "Product not found"

@app.delete("/product/{id}")
def delete_product(id:int, db:DBSession=Depends(get_db_session)):
    product=db.query(db_models.Product).filter(db_models.Product.id == id).first()
    if product:
        db.delete(product)
        db.commit()
        return "Product deleted"
    return "Product not found"

      


    