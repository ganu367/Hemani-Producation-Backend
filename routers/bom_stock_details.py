from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import database
import schemas
import models
import oauth2
from typing import List, Optional, Union
import os
from routers.utility import deleteFile
from os import getcwd, remove
import base64
from typing import Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from datetime import datetime
current_date = datetime.now()

router = APIRouter(prefix="/bom-stock-details", tags=["BoM STOCK DETAILS"])

get_db = database.get_db


@router.post("/create-bom-stk-details")
def CreateBomStockDetails(bom_stk_fields: schemas.BoMStockDetailsCreateList = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to create Process")
        else:
            try:

                # new_bom_stk = models.BOM_STOCK_DETAILS(
                #     **bom_stk_fields.dict())
                # db.add(new_bom_stk)
                # db.commit()
                # db.refresh(new_bom_stk)

                for i in bom_stk_fields.stock_details:
                    p1 = i.dict()
                    stk_details = models.BOM_STOCK_DETAILS(**p1)
                    db.add(stk_details)

                db.commit()

                return {"New bom stock added"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-bom-stk-details/{bom_id}/{process_id}")
def GetAllBomStockDetails(bom_id: int, process_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to create process")
        else:
            try:
                # data = db.query(models.BOM_STOCK_DETAILS.id, models.BOM_STOCK_DETAILS.process_id, models.BOM_STOCK_DETAILS.stock_id, models.BOM_STOCK_DETAILS.bom_quantity, models.BOM_STOCK_DETAILS.in_out, models.BOM_STOCK_DETAILS.uom, models.BOM_STOCK_DETAILS.created_by,
                #                 models.BOM_STOCK_DETAILS.created_on, models.BOM_STOCK_DETAILS.modified_by, models.BOM_STOCK_DETAILS.modified_on, models.StockMaster.item_name, models.BOM.bom_name, models.PROCESS.process_name).join(models.StockMaster, models.StockMaster.id == models.BOM_STOCK_DETAILS.stock_id).join(models.BOM, models.BOM.id == models.PROCESS.bom_id).join(models.PROCESS, models.PROCESS.id == models.BOM_STOCK_DETAILS.process_id)
                data = db.query(models.BOM_STOCK_DETAILS, models.StockMaster.item_name, models.BOM.bom_name, models.PROCESS.process_name).join(models.PROCESS, models.PROCESS.id == models.BOM_STOCK_DETAILS.process_id).join(
                    models.BOM, models.BOM.id == models.PROCESS.bom_id).join(models.StockMaster, models.StockMaster.id == models.BOM_STOCK_DETAILS.stock_id).filter(models.BOM_STOCK_DETAILS.bom_id == bom_id, models.BOM_STOCK_DETAILS.process_id == process_id)
                return (u._asdict() for u in data.all())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-bom-stk-details-by-ids/{ids}")
def GetBomStockDetailsByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to view Process")
        else:
            try:
                get_sc = db.query(models.BOM_STOCK_DETAILS.id, models.BOM_STOCK_DETAILS.process_id, models.BOM_STOCK_DETAILS.stock_id, models.BOM_STOCK_DETAILS.bom_quantity, models.BOM_STOCK_DETAILS.in_out, models.BOM_STOCK_DETAILS.uom, models.BOM_STOCK_DETAILS.created_by,
                                  models.BOM_STOCK_DETAILS.created_on, models.BOM_STOCK_DETAILS.modified_by, models.BOM_STOCK_DETAILS.modified_on, models.StockMaster.item_name, models.BOM.bom_name, models.PROCESS.process_name).join(models.StockMaster, models.StockMaster.id == models.BOM_STOCK_DETAILS.stock_id).join(models.BOM, models.BOM.id == models.PROCESS.bom_id).join(models.PROCESS, models.PROCESS.id == models.BOM_STOCK_DETAILS.process_id).filter(models.BOM_STOCK_DETAILS.id == ids)

                return (get_sc.first()._asdict())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.put("/update-bom-stk-details/{ids}")
def UpdateBomStockDetails(ids: int, bom_stk_fields: schemas.BoMStockDetailsUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to update Process")
        else:

            try:
                db.query(models.BOM_STOCK_DETAILS).filter(
                    models.BOM_STOCK_DETAILS.id == ids).update(bom_stk_fields.dict())
                db.commit()
                return {"bom stock fields are updated!"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.delete("/delete-bom-stk-details/{ids}")
def DeleteBomStockDetails(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to delete process")
        else:
            get_data = db.query(models.BOM_STOCK_DETAILS).filter(
                models.BOM_STOCK_DETAILS.id == ids)

            if not get_data.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="process data not found")
            else:
                try:
                    # get_process = db.query(models.PROCESS).filter(
                    #     models.PROCESS.process_id == ids)

                    # # count the child table
                    # if (get_process.count() == 0):
                    #     db.query(models.process).filter(
                    #         models.process.id == ids).delete()

                    get_data.delete()
                    db.commit()
                    return{f"process is deleted"}

                    # else:
                    #     return {f"delete related records {get_process.count()}"}

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")
