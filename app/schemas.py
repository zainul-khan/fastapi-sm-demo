#you can have a schema folder and seprate the schemas for different entities currently its a demo project so I am keeping a single file
from pydantic import BaseModel, ConfigDict, EmailStr, constr
from typing import List, Optional
from .constants import ACCESS_TOKEN_EXPIRY


#Schemas for user starts here

class UserBase(BaseModel):
    email: str
    name: str

class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: str 


class UserLogin(BaseModel):
    email: str
    password: str 


#Schemas for post starts here

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    address: Optional[str] = None  # Optional field
    # access_token: str
    # refresh_token: str

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserResponse]
    count: int


class PostBase(BaseModel):
    caption : str


class Post(PostBase):
    id : int
    owner_id  : int

    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id : int
    is_active : bool
    posts : list[Post] = []

    # class Config:
    #     from_attributesl = True
    model_config = ConfigDict(from_attributes=True)



class PostResponse(BaseModel):
    id: int
    caption: str
    media: str
    owner_id: int
    owner: UserResponse  # Embed the user information in the post

    class Config:
        from_attributes = True

class PostsListResponse(BaseModel):
    posts: List[PostResponse]

class PostLikeBase(BaseModel):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True


class PostBaseForLike(BaseModel):
    id: int
    caption: str
    owner_id: int

    class Config:
        from_attributes = True

class UserBaseForLike(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True


class PostLikeDetail(BaseModel):
    id: int
    user_id: int
    post_id: int
    user: UserBaseForLike
    post: PostBaseForLike

    class Config:
        from_attributes = True

class PostLikeListResponse(BaseModel):
    likes: List[PostLikeDetail]
