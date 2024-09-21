from fastapi import APIRouter, HTTPException, Header, status, Depends, Query, UploadFile, File, Request, Form
from typing import Annotated
from sqlalchemy import func, select
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload, aliased
from .. import schemas, models
from ..db import get_db
from ..dependencies import AccessTokenBearer
import os
from ..constants import MEDIA_FOLDER_PATH
from datetime import datetime
import time

access_token_bearer = AccessTokenBearer()

router = APIRouter(
    prefix='/post',
    tags = ['posts'],
)

os.makedirs(MEDIA_FOLDER_PATH, exist_ok=True)


@router.post("/create-post")
async def create_post(
    file: UploadFile = File(...),
    caption: str = Form(...),
    db: Session = Depends(get_db),
    token: dict = Depends(access_token_bearer)
):
    try:
        if not caption or not file:
            raise HTTPException(status_code=400, detail="Both caption and file are required")

        # Create media folder if it doesn't exist
        os.makedirs(MEDIA_FOLDER_PATH, exist_ok=True)

        # Generate a unique filename
        epoch_time = str(time.time())
        unique_filename = f"{token['user']['id']}{epoch_time}{file.filename}"
        file_path = os.path.join(MEDIA_FOLDER_PATH, unique_filename)
        print('file_path', file_path)

        database_url = f"/media/{unique_filename}"
        # Save the file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        # Create a new Post instance
        new_post = models.Post(
            caption=caption,
            owner_id=token['user']['id'],
            media=database_url
        )

        # Add and commit the new post to the database
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return {
           'statusCode': '201',
           'message': 'Post create successfully',
           'data': new_post
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/", response_model=schemas.PostsListResponse)
def read_posts(db: Session = Depends(get_db), token: dict = Depends(access_token_bearer)):
    try:
        posts = db.query(models.Post).options(joinedload(models.Post.owner)).all()
        count_query_of_total_posts = db.query(models.Post).count()
        print('count_query_of_total_posts', count_query_of_total_posts)
        return {"posts": posts}
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/{post_Id}", response_model=schemas.PostResponse)
async def read_post(post_Id: int, db:Session=Depends(get_db), token: dict = Depends(access_token_bearer)):
    try:
        post = db.query(models.Post).options(joinedload(models.Post.owner)).filter(models.Post.id == post_Id).first()
        if post is None:
            HTTPException(status_code=404, detail='Post was not found')
        return post
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.get("/{post_id}/likes", response_model=schemas.PostLikeListResponse)
async def get_post_likes(post_id: int, db: Session = Depends(get_db), token: dict = Depends(access_token_bearer)):

    # Query to get the total count of likes for the specified post
    count_query = db.query(models.PostLike).filter(models.PostLike.post_id == post_id).count()
    # Query PostLike and join with User and Post
    # Fetch all results
    likes_with_users_and_posts = db.query(models.PostLike).join(models.User, models.PostLike.user_id == models.User.id).join(models.Post, models.PostLike.post_id == models.Post.id).filter(models.PostLike.post_id == post_id)

    if not likes_with_users_and_posts:
        raise HTTPException(status_code=404, detail='No likes found for this post')
    print('likes_with_users_and_posts', likes_with_users_and_posts)

    
    return {"likes": likes_with_users_and_posts}


@router.get('/{post_id}/subquery')
async def get_post_like_count(post_id: int, db: Session = Depends(get_db),  token: dict = Depends(access_token_bearer)):
    try:

        # post_data = db.query(models.Post).filter(models.Post.id == post_id).first()
        # return {'post_data': post_data}
        PostLikeAlias = aliased(models.PostLike)

        # Create a subquery that counts the likes for each post
        like_count_subquery = (
            db.query(
                PostLikeAlias.post_id,
                func.count(PostLikeAlias.id).label("like_count")
            )
            .group_by(PostLikeAlias.post_id)
            .subquery()
        )

        # Join the subquery with the Post table
        post_with_like_count = (
            db.query(models.Post, like_count_subquery.c.like_count)
            .outerjoin(like_count_subquery, models.Post.id == like_count_subquery.c.post_id)
            .filter(models.Post.id == post_id)
            .first()
        )

        if not post_with_like_count:
            raise HTTPException(status_code=404, detail="Post not found")

        post_data, like_count = post_with_like_count

        result = {
            "caption": post_data.caption,
            "owner_id": post_data.owner_id,
            "id": post_data.id,
            "like_count": like_count or 0  # Handle the case where there are no likes
        }
        return result

    
    except Exception as e:
        return HTTPException(500, f"Someting went wrong {str(e)}")