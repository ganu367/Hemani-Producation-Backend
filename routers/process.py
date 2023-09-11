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

router = APIRouter(prefix="/process", tags=["Process"])

get_db = database.get_db


@router.post("/create-process")
def createProcess(process_fields: schemas.ProcessCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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

                new_process = models.PROCESS(
                    **process_fields.dict())
                db.add(new_process)
                db.commit()
                db.refresh(new_process)

                return {"New process added"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-process")
def GetAllProcess(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                data = db.query(models.BOM.bom_name, models.PROCESS.id, models.PROCESS.process_name, models.PROCESS.process_sequence, models.PROCESS.bom_id, models.PROCESS.created_by, models.PROCESS.created_on, models.PROCESS.modified_by, models.PROCESS.modified_on).join(
                    models.PROCESS, models.PROCESS.bom_id == models.BOM.id)
                return (u._asdict() for u in data.all())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-process-by-ids/{ids}")
def GetProcessByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                get_sc = db.query(models.BOM.bom_name, models.PROCESS.id, models.PROCESS.process_name, models.PROCESS.process_sequence, models.PROCESS.bom_id, models.PROCESS.created_by, models.PROCESS.created_on, models.PROCESS.modified_by, models.PROCESS.modified_on).join(
                    models.PROCESS, models.PROCESS.bom_id == models.BOM.id).filter(models.PROCESS.id == ids)
                return (get_sc.first()._asdict())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.put("/update-process/{ids}")
def UpdateProcess(ids: int, process_fields: schemas.ProcessUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                db.query(models.PROCESS).filter(
                    models.PROCESS.id == ids).update(process_fields.dict())
                db.commit()
                return {"Process fields are updated!"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.delete("/delete-process/{ids}")
def Deleteprocess(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
            get_process = db.query(models.PROCESS).filter(
                models.PROCESS.id == ids)

            if not get_process.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="process data not found")
            else:
                # try:

                    get_process.delete()
                    db.commit()

                  # count the child table

                    get_batch_actual_con = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                        models.BATCH_ACTUAL_CONSUMPTION.process_id == ids)

                    get_batch_actual_oh = db.query(models.BATCH_ACTUAL_OH).filter(
                        models.BATCH_ACTUAL_OH.process_id == ids)

                    if (get_batch_actual_con.count() == 0, get_batch_actual_oh.count() == 0):

                        db.query(models.Plants).filter(
                            models.Plants.id == ids).delete()
                        db.commit()
                        return{f"Plants is deleted"}

                    else:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f"delete related records: Batch Actual Con:{get_batch_actual_con.count()},Batch Actual OH: {get_batch_actual_oh.count()}")

                # except Exception as error:
                #     db.rollback()
                #     raise HTTPException(status_code=status.HTTP_302_FOUND,
                #                         detail=f"{str(error.orig)}")
