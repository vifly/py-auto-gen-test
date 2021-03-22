from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates/")


@app.get("/")
async def index_page(request: Request):
    return templates.TemplateResponse(
        "index.html", context={"request": request}
    )


@app.post("/somedata")
async def return_some_data(name: str = Form(...)):
    return {"data": "some data"}


@app.get("/synccall")
def sync_call():
    return {"sync": "OK"}


async def wont_in_generate_result():
    print("I don't define a path!")
