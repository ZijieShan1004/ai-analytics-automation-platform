from fastapi import HTTPException, status


# Raise a not found HTTP exception.
def raise_not_found(message: str = "Resource not found") -> None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)


# Raise a forbidden HTTP exception.
def raise_forbidden(message: str = "Forbidden") -> None:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)


# Raise a bad request HTTP exception.
def raise_bad_request(message: str = "Bad request") -> None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)