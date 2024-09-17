from fastapi import APIRouter

router = APIRouter(
    prefix="/transistors",
    tags=["transistors"]
)


@router.get("/list")
async def get_list():
    return {'message':  'spisok transistorov'}