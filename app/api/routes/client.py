import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import AM
from app.core.database import get_db
from app.crud.auth import require_role
from app.crud.client import (
    create_client,
    delete_client_by_id,
    get_client_by_id,
    get_client_by_email,
    get_clients,
    update_client,
)
from app.schemas.client import ClientCreate, ClientRead
from app.utils.exceptions import get_or_404

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientRead])
async def read_clients(
    session: AsyncSession = Depends(get_db), user=Depends(require_role(AM))
):
    clients = get_or_404(await get_clients(session), "clients not found")
    return clients


@router.get("/by_email/", response_model=ClientRead)
async def read_client(
    email: str = Query(...),
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    clients = get_or_404(await get_client_by_email(session, email), "Client not found")
    return clients


@router.post("/", response_model=ClientRead)
async def create_new_client(
    client_in: ClientCreate, session: AsyncSession = Depends(get_db)
):
    existing = await get_client_by_email(session, client_in.email)
    if existing:
        raise HTTPException(
            status_code=400, detail="Client with this email already exists"
        )
    return await create_client(session, client_in)

@router.get("/{client_id}", response_model=ClientRead)
async def read_client_by_id(
    client_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    client = get_or_404(await get_client_by_id(session, client_id), "Client not found")
    return client

@router.put("/{client_id}", response_model=ClientRead)
async def update_client_by_id(
    client_id: uuid.UUID,
    client_in: ClientCreate,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    client = get_or_404(await update_client(session, client_id, client_in), "Client not found")
    return client
    


@router.delete("/{client_id}", status_code=200)
async def delete_client(
    client_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    get_or_404(await delete_client_by_id(session, client_id), "Client not found")
    return {"message": "Client deleted"}


# @router.get("/{client_id}/deals")
# async def read_client_deals(client_id: str, session: AsyncSession = Depends(get_db)):
#     deals = get_or_404(await get_client_deals_by_id(session, client_id), "Deals not found")
#     return deals
  
    
    
    