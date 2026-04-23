from fastapi import FastAPI




app = FastAPI()



@app.get("/")
def home(): 
    return {"Messsage":"Start a new project!"}