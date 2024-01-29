from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session #Got to include .orm


#Pydantic(schema) and SQLAlchemy odels
#request is what the cliet pass
#The Query.update() method is a “bulk” operation
# 2:08
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
db is not take as query parameter but it is still returned
"""
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.post( "/user")
def create_user(request: schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = request.password) #request directly gives an error
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
 

@app.delete("/blog/{id}", status_code =status.HTTP_204_NO_CONTENT)
def destroy (id, db : Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    
    blog.delete(synchronize_session=False)
   
    db.commit()
    return "Deleted Succesfully!"

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request : schemas.Blog, db : Session = Depends(get_db)):
    blog =  db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Blog with id {id} not found")
    blog.update(request)
    db.commit()
    return "Updated Successfully"


@app.get("/blogs", response_model= list[schemas.ShowBlog])
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# db : Session = Depends(get_db)  => Database instance
@app.get("/blogs/{id}", status_code= 200, response_model= schemas.ShowBlog)
def show(id,response : Response,  db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"Blog with the id {id} is not available" )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail" : f"Blog with the id {id} is not available"}
    return blog


