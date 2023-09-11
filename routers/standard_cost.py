from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import database
import schemas
import models
import oauth2
from typing import List, Optional, Union
import psycopg2
import os
from routers.utility import deleteFile
from os import getcwd, remove
import base64
from typing import Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from datetime import datetime
current_date = datetime.now()

router = APIRouter(prefix="/scost", tags=["Standard Cost"])

get_db = database.get_db


@router.post("/create-standard-cost")
def createStandardCost(standard_cost_fields: schemas.StandardCostCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to create standarad cost")
        else:
            try:
                new_cost = models.StandardCost(
                    **standard_cost_fields.dict())
                db.add(new_cost)
                db.commit()
                db.refresh(new_cost)

                return {"New standard Cost added"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-standard-cost")
def GetAllStandardCost(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to view standarad cost")
        else:
            try:
                data = db.query(models.StockMaster.item_name,  models.StandardCost.id, models.StandardCost.uom, models.StandardCost.rate, models.StandardCost.stock_id, models.StandardCost.from_date, models.StandardCost.created_by, models.StandardCost.created_on, models.StandardCost.modified_by, models.StandardCost.modified_on).join(
                    models.StandardCost, models.StandardCost.stock_id == models.StockMaster.id)
                return (u._asdict() for u in data.all())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-standard-cost-by-ids/{ids}")
def GetStandardCostByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to view standarad cost")
        else:
            try:
                get_sc = db.query(models.StockMaster.item_name,  models.StandardCost.id, models.StandardCost.uom, models.StandardCost.rate, models.StandardCost.stock_id, models.StandardCost.from_date, models.StandardCost.created_by, models.StandardCost.created_on, models.StandardCost.modified_by, models.StandardCost.modified_on).join(
                    models.StandardCost, models.StandardCost.stock_id == models.StockMaster.id).filter(models.StandardCost.id
                                                                                                       == ids)
                return (get_sc.first()._asdict())

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.put("/update-standard-cost/{ids}")
def UpdateStandardCost(ids: int, standard_cost_fields: schemas.StandardCostUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to update standarad cost")
        else:

            try:
                db.query(models.StandardCost).filter(
                    models.StandardCost.id == ids).update(standard_cost_fields.dict())
                db.commit()
                return {"Standard Cost fields are updated!"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.delete("/delete-standard-cost/{ids}")
def DeleteStandardCost(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role in ["Purchase Manager", "Purchase Executive"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to delete standarad cost")
        else:
            get_sc = db.query(models.StandardCost).filter(
                models.StandardCost.id == ids)

            if not get_sc.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="standard cost data not found")
            else:
                try:

                    # count the child table
                    get_sc.delete()

                    # if (child_data.count() == 0):
                    #     db.query(models.StockMaster).filter(
                    #         models.StockMaster.id == ids).delete()
                    #     db.commit()
                    #     return{f"Stock Master is deleted"}

                    # else:
                    #     return {f"delete related records {child_data.count()}"}
                    db.commit()
                    return{f"Standars Cost is deleted"}

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")
