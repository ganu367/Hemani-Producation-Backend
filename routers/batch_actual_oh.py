from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, asc
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

router = APIRouter(prefix="/batch-actual-oh",
                   tags=["Batch Actual Overhead"])

get_db = database.get_db


@router.post("/create-batch-actual-oh")
def CreateActualBatchOH(batch_oh_fields: schemas.BatchActualOHCreateList = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]
    user_plantID = current_user_login.user["plantID"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to create batch actual overhead")
        else:
            try:
                for k in batch_oh_fields.oh_details:

                    get_count = db.query(models.BATCH_ACTUAL_OH).filter(
                        models.BATCH_ACTUAL_OH.plant_id == user_plantID)

                    if get_count.count() == 0:
                        batch_oh_number = 1
                    else:
                        last_id = db.query(func.max(models.BATCH_ACTUAL_OH.batch_actual_number_id)).filter(
                            models.BATCH_ACTUAL_OH.plant_id == user_plantID).first()

                        batch_oh_number = int(last_id[0]) + 1
                    print(batch_oh_number)

                    new_batch_oh = models.BATCH_ACTUAL_OH(
                        **k.dict(), entry_number=str(user_plantID)+"_"+str(batch_oh_number), batch_actual_number_id=batch_oh_number, plant_id=user_plantID, oh_cost=k.oh_rate*k.oh_quantity)

                    db.add(new_batch_oh)
                    # if get_count.count() == 0:
                    #     db.commit()
                db.commit()

                # db.refresh(new_batch_oh)

                return {"New batch actual Overhead created"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-actual-batch-oh-entries")
def GetAllActulaBatchOH(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to view all batch Actual Consumtpion")
        else:
            try:
                data = db.query(models.BATCH_ACTUAL_OH, models.BATCH.batch_number, models.PROCESS.process_name, models.Plants.plant_name
                                ).join(
                                    models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_OH.batch_id
                ).join(
                                    models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_OH.process_id
                ).join(
                                    models.Plants, models.Plants.id == models.BATCH_ACTUAL_OH.plant_id
                ).group_by(
                                    models.BATCH_ACTUAL_OH.entry_number
                )
                return (u._asdict() for u in data.all())

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-actual-batch-oh-by-ids/{entry}")
def GetActualBatchOH(entry: str, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
            get_batch_oh = db.query(models.BATCH_ACTUAL_OH).filter(
                models.BATCH_ACTUAL_OH.entry_number == entry)

            if get_batch_oh.first():
                try:

                    data = db.query(models.BATCH_ACTUAL_OH, models.BATCH, models.PROCESS, models.Plants).join(
                        models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_OH.batch_id
                    ).join(
                        models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_OH.process_id
                    ).join(
                        models.Plants, models.Plants.id == models.BATCH_ACTUAL_OH.plant_id
                    ).filter(
                        models.BATCH_ACTUAL_OH.entry_number == entry
                    )

                    # return (data.first()._asdict())
                    return (u._asdict() for u in data.all())

                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(e.orig)}")
            else:
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"Batch Actual overhead not found")


@router.put("/update-batch-actual-oh/{ids}")
def UpdateActualBatchOH(ids: int, batch_oh_fields: schemas.BatchActualOHUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                                detail="You don't have permmission to update Batch Actual")
        else:
            get_batch_oh = db.query(models.BATCH_ACTUAL_OH).filter(
                models.BATCH_ACTUAL_OH.id == ids)

            if get_batch_oh.first():
                try:
                    batch_oh_fields_dict = batch_oh_fields.dict()
                    batch_oh_fields_dict.update(
                        {"oh_cost": batch_oh_fields.oh_rate * batch_oh_fields.oh_quantity})

                    db.query(models.BATCH_ACTUAL_OH).filter(
                        models.BATCH_ACTUAL_OH.id == ids).update(batch_oh_fields_dict)

                    db.commit()
                    return {"Batch Actual Overhead fields are updated!"}

                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(e.orig)}")
            else:
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"Batch Actual not found")


@router.delete("/delete-actual-batch-oh/{ids}")
def DeleteActualBatchOH(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to delete Batch Actual ")
        else:
            get_data = db.query(models.BATCH_ACTUAL_OH).filter(
                models.BATCH_ACTUAL_OH.id == ids)

            if not get_data.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Batch Actual overhead data not found")
            else:
                try:
                    db.query(models.BATCH_ACTUAL_OH).filter(
                        models.BATCH_ACTUAL_OH.id == ids).delete()
                    db.commit()
                    return{f"Batch Actual overhead is deleted"}

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")


@router.delete("/delete-actual-batch-oh-entries/{entry}")
def DeleteActualBatchOH(entry: str, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to delete Batch Actual ")
        else:
            get_data = db.query(models.BATCH_ACTUAL_OH).filter(
                models.BATCH_ACTUAL_OH.entry_number == entry)

            if not get_data.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Batch Actual overhead data not found")
            else:
                try:
                    db.query(models.BATCH_ACTUAL_OH).filter(
                        models.BATCH_ACTUAL_OH.entry_number == entry).delete()
                    db.commit()
                    return{f"Batch Actual overhead is deleted"}

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")
