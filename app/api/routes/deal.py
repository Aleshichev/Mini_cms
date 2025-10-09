import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import AM
from app.core.database import get_db
from app.crud.auth import require_role
from app.crud.deal import get_all_deals, create_deal, delete_deal, get_deal_full, update_deal_by_id
from app.schemas.deal import DealCreate, DealRead, DealReadFull, DealUpdate
from app.utils.exceptions import get_or_404

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.get("/", response_model=list[DealReadFull])
async def read_deals(
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):

    deals = await get_all_deals(session)
    return deals

@router.post("/", response_model=DealRead)
async def create_new_deal(
    deal_in: DealCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    return await create_deal(session, deal_in)


@router.get("/{deal_id}", response_model=DealReadFull)
async def get_deal_details(
    deal_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    deal = await get_deal_full(session, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

@router.put("/{deal_id}", response_model=DealRead)
@router.patch("/{deal_id}", response_model=DealRead)
async def update_deal(
    deal_id: uuid.UUID,
    deal_in: DealUpdate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    deal = await update_deal_by_id(session, deal_id, deal_in)
    if not deal:
        raise HTTPException(404, detail="Project not found")
    return deal


@router.delete("/{deal_id}", status_code=200)
async def delete_deal_by_id(
    deal_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    get_or_404(await delete_deal(session, deal_id), "Deal not found")
    return {"message": "Deal deleted"}
