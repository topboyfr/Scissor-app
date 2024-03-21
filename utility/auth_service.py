from typing import Generator
from jose import jwt
from fastapi import HTTPException, status, Depends
from database import database, model
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing_extensions import Annotated  
from utility.app_service import db_session

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY = "topboysupersecretkey"
ALGORITHM = "HS256"

def decode_token(request, db):
        try:
            token = request.cookies.get('access_token')
            if token is None:
                return None
            
            payload = jwt.decode(token, SECRET_KEY, algorithms =[ALGORITHM])
            username:str = payload.get("sub") #"sub" is a field holding the username/email address
            user = db.query(model.User).filter(model.User.email==username).first()
            if user is None:
                return None
              #return the user as authenticated
            return user
    
        except Exception as e:
            return None
        
    
def auth_user(username:str, password:str,expires_delta:timedelta, db: db_session):
        get_user=db.query(model.User).filter(model.User.email==username and bcrypt_context.verify(password,model.User.password)==True)
        if get_user.first():
            encode = {'sub':username}
            expires = datetime.utcnow()+expires_delta
            encode.update({'exp': expires})
            jwt_token= jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
            return jwt_token
        
        return False