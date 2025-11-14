from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, security

router = APIRouter()


@router.post("/", response_model=schemas.AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account: schemas.AccountCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    db_account = models.Account(**account.dict(), owner_id=current_user.id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/", response_model=List[schemas.AccountResponse])
def read_accounts(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    accounts = db.query(models.Account).filter(
        models.Account.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return accounts


@router.get("/{account_id}", response_model=schemas.AccountResponse)
def read_account(
    account_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.owner_id == current_user.id
    ).first()
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account


@router.put("/{account_id}", response_model=schemas.AccountResponse)
def update_account(
    account_id: int,
    account_update: schemas.AccountUpdate,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    db_account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.owner_id == current_user.id
    ).first()
    if db_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    update_data = account_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int,
    current_user: models.User = Depends(security.get_current_user),
    db: Session = Depends(get_db)
):
    db_account = db.query(models.Account).filter(
        models.Account.id == account_id,
        models.Account.owner_id == current_user.id
    ).first()
    if db_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    db.delete(db_account)
    db.commit()
    return None
