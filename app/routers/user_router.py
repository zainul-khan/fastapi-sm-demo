from fastapi import APIRouter, HTTPException, status, Depends, Query, status
from datetime import timedelta
from sqlalchemy.orm import Session
from .. import schemas, models
from ..db import get_db
from ..utils import generate_password_hash, verify_password_hash, create_access_token
from ..constants import REFRESH_TOKEN_EXPIRY
from ..dependencies import AccessTokenBearer


router = APIRouter(
    prefix='/user',
    tags = ['users']
)

access_token_bearer = AccessTokenBearer()


@router.post("/sign-up")
def sign_up_user(user:schemas.UserSignUp, db:Session=Depends(get_db)):
    try:
        # Check if the user already exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the user's password
        hashed_pass = generate_password_hash(user.password)

        # Create a new User instance
        new_user = models.User(
            name=user.name,
            email=user.email,
            password=hashed_pass
        )

        # Add and commit the new user to the database
        db.add(new_user)
        db.commit()

        # Refresh to get the latest state of the user
        db.refresh(new_user)

        # Prepare user data for token generation
        user_data = {
            'id': new_user.id,
            'email': new_user.email
        }

        # Generate tokens
        access_token = create_access_token(user_data, refresh=False)
        refresh_token = create_access_token(user_data, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY), refresh=True)

        # Return the response
        return {
            'statusCode': 201,
            'message': 'User fetched successfully',
            'data': {new_user},
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
       
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print('error=>', e)
        raise HTTPException(status_code=500, detail="Something went wrong")


@router.post('/login')
def login_user(user: schemas.UserLogin, db:Session=Depends(get_db)):
    try: 
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid Credentials")
        
        verify_password = verify_password_hash(user.password, db_user.password)
        if not verify_password:
            raise HTTPException(status_code=400, detail="Invalid Credentials")

        user_data = {
            'id': db_user.id,
            'email': db_user.email
        }

        # Generate tokens
        access_token = create_access_token(user_data, refresh=False)
        refresh_token = create_access_token(user_data, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY), refresh=True)
        return {
            "statusCode": status.HTTP_200_OK,
            "detail": 'User logged in successfully',
            "data": db_user,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print('error=>', e)
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get('/')
def get_all_users(db: Session = Depends(get_db),  username: str = Query(None), email: str = Query(None), skip: int = Query(0), limit: int = Query(10), token: dict = Depends(access_token_bearer)):
    try:
        print('tokenfinal', token['user']['id'])
        query = db.query(models.User)
        if username:
            query = query.filter(models.User.name.like(f"%{username}%"))
        if email:
            query = query.filter(models.User.email.like(f"%{email}%"))
        total_count = query.count()
        users = query.order_by(models.User.id.desc()).offset(skip).limit(limit).all()
        return {
                "statusCode": status.HTTP_200_OK,
                'message': 'Users fetched successfully',
                'users': users, 
                'count': total_count, 
                }
       
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print('error=>', e)
        raise HTTPException(status_code=500, detail="Something went wrong")
