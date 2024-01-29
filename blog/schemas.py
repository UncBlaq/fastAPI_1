from pydantic import BaseModel
#Pydantic gave us the nice request field
class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode = True     #This hides the id from respons body


class User(BaseModel):
    name : str
    password : str
    email : str

   