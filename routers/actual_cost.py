from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import database
import schemas
import models
import oauth2
from datetime import datetime

current_date = datetime.now()

router = APIRouter(prefix="/acost", tags=["Actual Cost"])

get_db = database.get_db


@router.post("/create-actual-cost")
def createActualCost(actual_cost_fields: schemas.ActualCostCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to create actual cost")
        else:
            try:
                new_cost = models.ActualCost(
                    **actual_cost_fields.dict())
                db.add(new_cost)
                db.commit()
                db.refresh(new_cost)

                return {"New Actual Cost added"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-actual-cost")
def GetAllActualCost(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to view actual cost")
        else:
            try:
                data = db.query(models.StockMaster.item_name, models.ActualCost.id, models.ActualCost.uom, models.ActualCost.rate, models.ActualCost.stock_id, models.ActualCost.from_date, models.ActualCost.created_by, models.ActualCost.created_on, models.ActualCost.modified_by, models.ActualCost.modified_on).join(
                    models.ActualCost, models.ActualCost.stock_id == models.StockMaster.id)
                return (u._asdict() for u in data.all())

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-actual-cost-by-ids/{ids}")
def GetActualCostByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to view actual cost")
        else:
            try:
                get_sc = db.query(models.StockMaster.item_name, models.ActualCost.id, models.ActualCost.uom, models.ActualCost.rate, models.ActualCost.stock_id, models.ActualCost.from_date, models.ActualCost.created_by, models.ActualCost.created_on, models.ActualCost.modified_by, models.ActualCost.modified_on).join(
                    models.ActualCost, models.ActualCost.stock_id == models.StockMaster.id).filter(models.ActualCost.id
                                                                                                   == ids)
                return (get_sc.first()._asdict())

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.put("/update-actual-cost/{ids}")
def UpdateActualCost(ids: int, actual_cost_fields: schemas.ActualCostUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to update actual cost")
        else:

            try:
                db.query(models.ActualCost).filter(
                    models.ActualCost.id == ids).update(actual_cost_fields.dict())
                db.commit()
                return {"Actual Cost fields are updated!"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.delete("/delete-actual-cost/{ids}")
def DeleteActualCost(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to delete actual cost")
        else:
            get_sc = db.query(models.ActualCost).filter(
                models.ActualCost.id == ids)

            if not get_sc.first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Actual cost data not found")
            else:
                try:
                    get_sc.delete()
                    db.commit()
                    return{f"Actual Cost is deleted"}

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")
