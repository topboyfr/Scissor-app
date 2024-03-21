from fastapi import APIRouter, Response, Depends, Request, HTTPException
from schema import link, user
from typing_extensions import Annotated
from utility.app_service import db_session
from utility import auth_service
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette import status
from fastapi.templating import Jinja2Templates
                            
auth_router= APIRouter(prefix="/auth",tags=["auth"])

templates = Jinja2Templates(directory="templates")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@auth_router.post("/token",response_model=link.Token)
async def create_token(
    response:Response,
    form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
    db:db_session
):
    token = auth_service.auth_user(form_data.username, form_data.password, timedelta(minutes=60), db)
    
    if token == False :

        return False
    
    response.set_cookie(key="access_token",value= token,httponly=True)

    return True

@auth_router.get("/login", response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse("login.html",{"request": request})

@auth_router.post("/login", response_class= HTMLResponse)
async def login(request:Request, db:db_session):

    messages=[]
    try: 
        form = user.loginForm(request)
        await form.create_auth_form()
        response = RedirectResponse("/users/dashboard", status_code= status.HTTP_302_FOUND)
        validate_user_cookie = await create_token(response = response, form_data= form, db = db)

        if not validate_user_cookie:
            messages.append("invalid credentials")
            
            return templates.TemplateResponse("login.html", {"request":request, "messages":messages})
        
        return response
    except HTTPException:
        messages.append("internal server error")
        return  templates.TemplateResponse("login.html", {"request":request, "messages":messages})
    
    
@auth_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):

    messages=[]

    messages.append("Logout successful")
    response = templates.TemplateResponse("login.html", {"request": request, "messages": messages})
    response.delete_cookie(key="access_token")
    return response

