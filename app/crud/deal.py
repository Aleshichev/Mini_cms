import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.deal import Deal
from app.schemas.deal import DealCreate
from app.utils.exceptions import handle_db_exceptions


async def get_deal(session: AsyncSession, deal_id: uuid.UUID) -> Deal | None:
    stmt = select(Deal).where(Deal.id == deal_id)
    result = await session.execute(stmt)
    return result.scalars().first()


@handle_db_exceptions
async def create_deal(session: AsyncSession, deal_in: DealCreate) -> Deal:
    deal = Deal(
        id=uuid.uuid4(),
        title=deal_in.title,
        description=deal_in.description,
        status=deal_in.status,
        client_id=deal_in.client_id,
        manager_id=deal_in.manager_id,
        project_id=deal_in.project_id,
    )
    session.add(deal)
    await session.commit()
    await session.refresh(deal)
    return deal


async def get_deal_full(session: AsyncSession, deal_id: uuid.UUID) -> Deal | None:
    stmt = (
        select(Deal)
        .where(Deal.id == deal_id)
        .options(joinedload(Deal.client), joinedload(Deal.manager))
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def update_deal_by_id(
    session: AsyncSession, deal_id: uuid.UUID, deal_in: DealCreate
) -> Deal | None:
    deal = await get_deal(session, deal_id)
    if not deal:
        return None
    update_data = deal_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(deal, field, value)

    await session.commit()
    await session.refresh(deal)
    return deal


async def delete_deal(session: AsyncSession, deal_id: uuid.UUID) -> None:
    deal = await get_deal(session, deal_id)
    if not deal:
        return None
    await session.delete(deal)
    await session.commit()
    return deal
