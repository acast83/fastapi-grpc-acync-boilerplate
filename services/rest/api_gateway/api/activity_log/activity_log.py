from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_activity_log() -> dict:
    return {"message": "activity_log"}
