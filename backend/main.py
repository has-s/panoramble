from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


backend = FastAPI()
tests = Jinja2Templates(directory="backend/tests")
templates = Jinja2Templates(directory="backend/templates")

@backend.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return tests.TemplateResponse("test_main.html", {"request": request})

@backend.get("/api/{name}") #look at test_main.http | Use as Postman
async def say_hello(name: str):
    return {"message": f"You are at: /api/{name}"}
