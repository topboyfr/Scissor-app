"""CRUD operations."""

##from config.config import get_settings
from starlette.datastructures import URL
from schema import link
from utility import keygen
from database import model
from sqlalchemy.orm import Session
from datetime import datetime



base_url = "http://127.0.0.1:8000/"



def create_and_save_url(db, title, url, user_id) -> link.URL:
    
    """Create URL in the Database."""
    #generate unique key
    key = keygen.create_unique_random_key(db)

    #database dump
    db_url = model.URL(
        title = title,
        target_url= url,
        key= key,
        date_created = datetime.now().date(), 
        owner_id = user_id
    )
    db.add(db_url)
    db.commit()
    return db_url

#function 2
def get_url_by_key(url_key:str, db:Session) -> model.Link:
    """Return a URL by specified key."""
    
    return (
        db.query(model.URL)
        .filter(model.URL.key == url_key)
        .first()
    )


def update_db_clicks(db: Session, db_url: model.Link) -> model.Link:
    """Update the count of times the link has been visited."""
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url    
