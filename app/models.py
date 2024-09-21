from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(255),index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    address = Column(String(255), nullable=True)
    is_active = Column(Boolean,default=True)
    status = Column(String(255), default='Active')
    posts = relationship("Post",back_populates="owner")
    liked_posts = relationship("PostLike", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    media = Column(String(255), index=True)

    owner = relationship("User",back_populates="posts")
    likes = relationship("PostLike", back_populates="post")


class PostLike(Base):
    __tablename__ = "post_likes"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="liked_posts")


