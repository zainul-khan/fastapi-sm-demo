from fastapi import APIRouter, HTTPException, status, Depends, Query, status
from datetime import timedelta
from sqlalchemy.orm import Session
from .. import models
from ..utils import decode_token, create_access_token
from ..constants import REFRESH_TOKEN_EXPIRY
from ..db import get_db


router = APIRouter(
    tags = ['refresh_token']
)

@router.get('/refresh-token')
async def refresh_access_token(db:Session=Depends(get_db), refresh_access_token: str = Query(None)):
    try:
        print('refresh_token', refresh_access_token)
        token_data, error = decode_token(refresh_access_token)

        if not token_data or error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        
        if (token_data['refresh'] == False):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token passed but refresh token was needed")

        db_user = db.query(models.User).filter(models.User.id == token_data['user']['id']).first()

        if not db_user:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid id extracted from token") 

        user_data = {
            'id': db_user.id,
            'email': db_user.email
        }

        access_token = create_access_token(user_data, refresh=False)

        return {
            'access_token': access_token
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print('error=>', e)
        raise HTTPException(status_code=500, detail="Something went wrong")