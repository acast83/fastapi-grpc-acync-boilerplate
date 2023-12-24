from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health() -> dict:
    return {"healthy": True}
