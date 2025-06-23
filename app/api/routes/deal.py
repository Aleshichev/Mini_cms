from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.deal import DealCreate, DealRead, DealReadFull
from app.crud.deal import create_deal, get_deal_full
from app.core.database import get_db
import uuid

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.post("/", response_model=DealRead)
async def create_new_deal(
    deal_in: DealCreate,
    session: AsyncSession = Depends(get_db),
):
    return await create_deal(session, deal_in)


@router.get("/{deal_id}", response_model=DealReadFull)
async def get_deal_details(deal_id: uuid.UUID, session: AsyncSession = Depends(get_db) ):
    deal = await get_deal_full(session, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal
