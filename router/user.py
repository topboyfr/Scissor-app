from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
from database.model import User, Link
from schema import user
from utility.auth_service import bcrypt_context, decode_token
from utility.app_service import db_session, functions
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


user_router = APIRouter(prefix = "/users", tags=["users"])

templates = Jinja2Templates(directory="templates")

@user_router.get("/create_user")
async def add_user(request:Request):
    
    #return "user confirmed"
    return templates.TemplateResponse("registration.html",{"request": request})

@user_router.post("/create_user")
async def add_user(request:Request, 
    first_name: str=Form(...),
    last_name: str=Form(...),
    email: str=Form(...),
    password: str=Form(...),
    password2: str=Form(...),
    db:Session=Depends(functions.get_db)):

    messages=[]

    if password != password2:
        messages.append("password doesn't match!")
        return templates.TemplateResponse('registration.html',{'request':request,'messages':messages})

    if len(password) < 8:
        messages.append("password should be above 8 characters")
        return templates.TemplateResponse('registration.html',{'request':request,'messages':messages})


    emails = db.query(User).filter(User.email==email).first()
    if emails: 
        messages.append("email already in use!")
        return templates.TemplateResponse('registration.html',{'request':request,'messages':messages})
    
    new_user = User(
        first_name= first_name,
        last_name= last_name,
        email = email,
        password = bcrypt_context.hash(password),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    messages.append("successful")
    return templates.TemplateResponse('login.html',{'request':request,'messages':messages})
    # raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=my_user)

@user_router.get("/FAQs")
async def FAQs(request:Request):
    
    #return "user confirmed"
    return templates.TemplateResponse("faq.html",{"request": request})

@user_router.get("/dashboard",response_class= HTMLResponse)
async def dashboard(request:Request,
    db:Session=Depends(functions.get_db)):
    user =  decode_token(request,db)
    if user is None:
        return templates.TemplateResponse("login.html",{"request": request})
    
    links = db.query(Link).filter(Link.owner_id==user.id).all()

    print (links, user)

    return templates.TemplateResponse("dashboard.html",
        {"request": request, "user": user,"links": links})

