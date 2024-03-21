from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String, nullable= False)
    last_name = Column(String, nullable= False)
    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
     
    owner = relationship("Link", back_populates = "url")

class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String, nullable= False, default="url link")
    target_link = Column(String, nullable= False)
    key = Column(String, nullable= False)
    visits = Column(Integer, default = 0)
    date_created = Column(Date, nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    url = relationship("User" , back_populates = "owner")
