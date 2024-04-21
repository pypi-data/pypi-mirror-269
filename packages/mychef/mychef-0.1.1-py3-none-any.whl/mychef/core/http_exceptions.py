from fastapi import HTTPException, status

InvalidCredentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class EntityAlreadyExists(HTTPException):
    def __init__(self, detail: str):
        return super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
