import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.client import Client
from app.models.deal import Deal
from app.schemas.client import ClientCreate
from app.utils.exceptions import handle_db_exceptions


async def get_clients(session: AsyncSession) -> list[Client]:
    result = await session.execute(select(Client))
    return result.scalars().all()


async def get_client_by_email(session: AsyncSession, email: str) -> Client | None:
    stmt = select(Client).where(Client.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_client_by_id(
    session: AsyncSession, client_id: uuid.UUID
) -> Client | None:
    stmt = (
        select(Client).options(selectinload(Client.deals)).where(Client.id == client_id)
    )
    result = await session.execute(stmt)
    return result.scalars().first()

# async def get_client_deals_by_id(session: AsyncSession, client_id: uuid.UUID) -> list[Client] | None:
#     stmt = select(Deal).where(Deal.client_id == client_id)
#     result = await session.execute(stmt)
#     deals = result.scalars().all()
#     return deals
    
    
async def update_client(
    session: AsyncSession, client_id: uuid.UUID, client_in: ClientCreate
) -> Client | None:
    client = await get_client_by_id(session, client_id)
    if not client:
        return None

    client.full_name = client_in.full_name
    client.email = client_in.email
    client.phone = client_in.phone
    client.telegram_id = client_in.telegram_id

    session.add(client)
    await session.commit()
    await session.refresh(client)
    return client


@handle_db_exceptions
async def create_client(session: AsyncSession, client_in: ClientCreate) -> Client:
    client = Client(
        id=uuid.uuid4(),
        full_name=client_in.full_name,
        email=client_in.email,
        phone=client_in.phone,
        telegram_id=client_in.telegram_id,
    )
    session.add(client)
    await session.commit()
    await session.refresh(client)
    return client


async def delete_client_by_id(session: AsyncSession, client_id: uuid.UUID) -> None:
    client = await session.get(Client, client_id)
    if not client:
        return None

    await session.delete(client)
    await session.commit()
    return client
