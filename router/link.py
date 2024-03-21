import validators
from fastapi import APIRouter, Request, Depends, status, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from utility.rate_limit import rate_limited
from utility import auth_service, keygen
from database import database, model
from datetime import datetime


templates = Jinja2Templates(directory="templates")


link_router = APIRouter(tags=["links"])

@link_router.get("/",response_class=HTMLResponse)
async def add_link(request:Request):
    
    return templates.TemplateResponse("index.html",{"request":request})

    # raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=my_user)

@link_router.get("/create_url", response_class=HTMLResponse)
@rate_limited(max_calls=3, time_frame=60)
async def create_url(
    request: Request,
    db:Session=Depends(database.get_db)
    ):
    
    # authentication
    user = auth_service.decode_token(request, db)
    if not user:
        messages = []
        
        messages.append("Session Expired, Login")
        return templates.TemplateResponse("login.html", {"request": request, "user": user})
    
    
    return templates.TemplateResponse(
        "create_url.html", 
        {"request": request, "user": user}
    )

@link_router.post("/create_url", response_class=HTMLResponse)
@rate_limited(max_calls=3, time_frame=60)
async def create_url_post(
    request: Request,
    target_url: str = Form(...),
    title: str = Form(...),
    db:Session=Depends(database.get_db)
):
    
    messages = []
    
    # authentication
    user = auth_service.decode_token(request, db)
    
    if not user:
        messages.append("Session Expired, Login")
        return templates.TemplateResponse("login.html", {"request": request, "messages": messages})
    
    if not validators.url(target_url):
        messages.append("Invalid destination url, kindly include: https:// or http://")
        return templates.TemplateResponse("create_url.html", 
            {
                "request": request,
                "messages": messages, 
                "user": user, 
                "target_url": target_url,
                "title": title
            }
        )
    
   
    key = keygen.create_unique_random_key(db)

    #database dump
    db_url = model.Link(
        title = title,
        target_url= target_url,
        key= key,
        date_created = datetime.now().date(), 
        owner_id = user.id
    )
    db.add(db_url)
    db.commit() 
    return RedirectResponse("/users/dashboard", status_code=status.HTTP_302_FOUND)

@link_router.get("/customize/{url_key}", response_class=HTMLResponse)
@rate_limited(max_calls=3, time_frame=60)
async def customise(
    request: Request, 
    url_key:str, 
    db:Session=Depends(database.get_db)
):
    messages = []
    
    # authentication
    user = auth_service.auth_user(request, db)
    if not user:
        messages.append("session expired, kindly Login")
        return templates.TemplateResponse("login.html", {'request':Request, 'messages': messages})
    
    url_key = db.query(model.Link).filter(model.Link.target_link == url_key).first()
    
    return templates.TemplateResponse("Customize.html", {"request": request, "user": user, 'url_key': url_key, "messages": messages})