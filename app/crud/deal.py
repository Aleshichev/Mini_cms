import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.deal import Deal
from app.schemas.deal import DealCreate
from sqlalchemy.orm import joinedload


async def get_deal(session: AsyncSession, deal_id: uuid.UUID) -> Deal | None:
    stmt = select(Deal).where(Deal.id == deal_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_deal(session: AsyncSession, deal_in: DealCreate) -> Deal:
    deal = Deal(
        id=uuid.uuid4(),
        title=deal_in.title,
        description=deal_in.description,
        status=deal_in.status,
        client_id=deal_in.client_id,
        manager_id=deal_in.manager_id,
    )
    session.add(deal)
    await session.commit()
    await session.refresh(deal)
    return deal


async def get_deal_full(session: AsyncSession, deal_id: uuid.UUID) -> Deal | None:
    stmt = (
        select(Deal)
        .where(Deal.id == deal_id)
        .options(
            joinedload(Deal.client),
            joinedload(Deal.manager)
            )
    )
    result = await session.execute(stmt)
    return result.scalars().first()
