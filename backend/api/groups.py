from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_session
from backend.database.crud import crud_group


router = APIRouter()


@router.get("/all")
async def get_all_groups(session: AsyncSession = Depends(get_session)):
    groups = await crud_group.get_all(session, limit=-1)
    return {"groups": groups}


@router.get("/closest/{group_name}")
async def get_closest_name(group_name: str, session: AsyncSession = Depends(get_session)):
    group = await crud_group.find_closest(session, group_name)
    return group


@router.get("/{group_id}")
async def get_group(group_id: int, session: AsyncSession = Depends(get_session)):
    group = await crud_group.get(session, group_id)
    return group
