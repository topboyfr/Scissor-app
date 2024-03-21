from fastapi import FastAPI
from router import user, link, login
from database.database import engine
from database.model import Base
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI(openapi_tags=[ 
    {"name":"users","description":"user routes"},
    {"name":"links","description":"links"},
    {"name":"auth","description":"auth route"}
])

templates = Jinja2Templates(directory="templates")

app.mount("/static",StaticFiles(directory="static"), name="static")
app.mount("/static/css", StaticFiles(directory="static/css"), name="css")

Base.metadata.create_all(bind = engine)

app.include_router(user.user_router)
app.include_router(link.link_router)
app.include_router(login.auth_router)