from fastapi import APIRouter

router = APIRouter()


# Return health status for the API.
@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}