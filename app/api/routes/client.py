from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.client import ClientCreate, ClientRead
from app.crud.client import create_client, get_client_by_email
from app.core.database import get_db

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/", response_model=ClientRead)
async def create_new_client(
    client_in: ClientCreate,
    session: AsyncSession = Depends(get_db)
):
    if client_in.email:
        existing = await get_client_by_email(session, client_in.email)
        if existing:
            raise HTTPException(status_code=400, detail="Client with this email already exists")
    return await create_client(session, client_in)
