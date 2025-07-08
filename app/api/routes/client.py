from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.client import ClientCreate, ClientRead
from app.crud.auth import require_role
from app.crud.client import (
    create_client,
    get_client_by_email,
    get_clients,
    delete_client_by_id,
)
from app.core.database import get_db
from app.utils.exceptions import get_or_404
from app.core.config import AM

import uuid

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


@router.delete("/{client_id}", status_code=200)
async def delete_client(
    client_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(require_role(AM)),
):
    get_or_404(await delete_client_by_id(session, client_id), "Client not found")
    return {"message": "Client deleted"}
