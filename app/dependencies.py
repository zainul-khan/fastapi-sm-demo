from fastapi import status, Depends
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token

security = HTTPBearer()

class AccessTokenBearer:
    def __init__(self):
        self.security = HTTPBearer()

    async def __call__(self, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
        if credentials is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer authentication required")
        
        token = credentials.credentials

        try:
            decoded_token, error = decode_token(token)
            if not decode_token or error:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
            return decoded_token
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")