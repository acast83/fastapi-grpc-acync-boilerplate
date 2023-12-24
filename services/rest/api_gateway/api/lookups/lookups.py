from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_lookups() -> dict:
    return {"message": "lookups"}
