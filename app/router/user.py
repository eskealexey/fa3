from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/all_users")
async def get_all_users():
    pass


@router.post("/create")
async def create_user():
    pass


@router.put("/update")
async def update_user():
    pass


@router.delete("/delete")
async def delete_user():
    pass
