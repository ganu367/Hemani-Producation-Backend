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
import pytz
utc = pytz.UTC

current_date = datetime.now()

router = APIRouter(prefix="/batch", tags=["Batch"])

get_db = database.get_db


@router.post("/create-batch")
def Createbatch(batch_fields: schemas.BatchCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]
    user_plantID = current_user_login.user["plantID"]
    print(user_plantID)

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to create batch")
        else:
            # try:

            get_count = db.query(models.BATCH).filter(
                models.BATCH.plant_id == user_plantID)

            if get_count.count() == 0:
                batch_number = 1
            else:
                last_id = db.query(func.max(models.BATCH.batch_number_id)).filter(
                    models.BATCH.plant_id == user_plantID).first()

                batch_number = int(last_id[0]) + 1

            new_batch = models.BATCH(
                **batch_fields.dict(), batch_number=str(user_plantID)+"_"+str(batch_number), batch_number_id=batch_number, plant_id=user_plantID)

            db.add(new_batch)
            db.commit()
            db.refresh(new_batch)

            return {"New batch created"}

            # except Exception as e:
            #     db.rollback()
            #     raise HTTPException(status_code=status.HTTP_302_FOUND,
            #                         detail=f"{str(e.orig)}")


@router.get("/get-all-batch")
def GetAllBatch(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to view all batch")
        else:
            try:
                data = db.query(models.BATCH, models.BOM.bom_name, models.StockMaster.item_name, models.Plants.plant_name).join(models.BOM, models.BOM.id == models.BATCH.bom_id).join(models.StockMaster, models.StockMaster.id == models.BOM.stock_id).join(
                    models.Plants, models.Plants.id == models.BATCH.plant_id)
                return (u._asdict() for u in data.all())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-batch-by-ids/{ids}")
def GetBatchByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                get_sc = db.query(models.BATCH, models.BOM, models.StockMaster, models.Plants).join(models.BOM, models.BOM.id == models.BATCH.bom_id).join(models.StockMaster, models.StockMaster.id == models.BOM.stock_id).join(
                    models.Plants, models.Plants.id == models.BATCH.plant_id).filter(models.BATCH.id
                                                                                     == ids)
                return (get_sc.first()._asdict())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.put("/update-batch/{ids}")
def UpdateBatch(ids: int, batch_fields: schemas.BatchUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                                detail="You don't have permmission to update ")
        else:

            try:
                db.query(models.BATCH).filter(
                    models.BATCH.id == ids).update(batch_fields.dict())
                db.commit()
                return {"Batch fields are updated!"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")

@router.put("/update-batch-status/{ids}")
def UpdateBatchStatus(ids: int, batch_fields: schemas.BatchUpdateStatus = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                                detail="You don't have permmission to update ")
        else:
            get_batch = db.query(models.BATCH).filter(
                models.BATCH.id == ids)

            if get_batch.first().status == "closed":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="this batch already closed")
            else:
                if not (batch_fields.end_date >= utc.localize(get_batch.first().start_date)):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail="can't update status of batch")
                else:
                    try:

                        batch_fields_dict = batch_fields.dict()
                        batch_fields_dict.update(
                            {"end_date": batch_fields.end_date, "status": "closed"})

                        db.query(models.BATCH).filter(
                            models.BATCH.id == ids).update(batch_fields_dict)
                        db.commit()

                        return {"This batch closed now!"}

                    except Exception as e:
                        db.rollback()
                        raise HTTPException(status_code=status.HTTP_302_FOUND,
                                            detail=f"{str(e.orig)}")


@router.delete("/delete-batch/{ids}")
def DeleteBatch(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to delete batch")
        else:
            get_data = db.query(models.BATCH).filter(
                models.BATCH.id == ids)

            if not get_data.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Batch data not found")
            else:
                try:
                    get_batch_actual_cons = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                        models.BATCH_ACTUAL_CONSUMPTION.process_id == ids)

                    get_batch_actual_oh = db.query(models.BATCH_ACTUAL_OH).filter(
                        models.BATCH_ACTUAL_OH.process_id == ids)

                    # count the child table
                    if ((get_batch_actual_cons.count()) == 0 and (get_batch_actual_oh.count()) == 0):
                        db.query(models.BATCH).filter(
                            models.BATCH.id == ids).delete()
                        db.commit()
                        return{f"Batch is deleted"}

                    else:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f"delete related records of batch actual consumption: {get_batch_actual_cons.count()} and batch actual Overhead: {get_batch_actual_oh.count()}")

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")
