import os
import uuid
from typing import Dict

import jwt
from fastapi import Depends, status
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class TokenUtils:
    @staticmethod
    def decode_token(request=None, token=None) -> Dict[str, str | uuid.UUID]:
        if not token and not request:
            raise ValueError("either request or token must be provided")
        if not token:
            token = request.headers["Authorization"]
            token = token.split(" ")[1]
        try:
            jwt_key = os.getenv("JWT_KEY")
            algorithm = os.getenv("ALGORITHM")
            decoded_token = jwt.decode(token, jwt_key, algorithms=[algorithm])

            return {"id_user": uuid.UUID(decoded_token["id"]), "token": token}

        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def encode_token(data: dict) -> jwt.PyJWT:
        jwt_key = os.getenv("JWT_KEY")
        algorithm = os.getenv("ALGORITHM")
        token = jwt.encode(data, key=jwt_key, algorithm=algorithm)

        return token


class AuthenticationRequired(TokenUtils):
    def __init__(
            self,
            token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),

    ) -> None:
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="TOKEN_NOT_PROVIDED")
        self.decode_token(token=token.credentials)
