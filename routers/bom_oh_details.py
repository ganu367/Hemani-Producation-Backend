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

router = APIRouter(prefix="/bom-oh-details", tags=["BoM OH DETAILS"])

get_db = database.get_db


@router.post("/create-bom-oh-details")
def CreateBomOHDetails(bom_oh_fields: schemas.BoMOHCreateList = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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

                # new_bom_oh = models.BOM_OH_DETAILS(
                #     **bom_oh_fields.dict())
                # db.add(new_bom_oh)
                # db.commit()
                # db.refresh(new_bom_oh)

                for i in bom_oh_fields.oh_details:
                    p1 = i.dict()
                    oh_details = models.BOM_OH_DETAILS(
                        **p1, oh_cost=i.oh_rate*i.oh_quantity)
                    db.add(oh_details)

                db.commit()

                return {"New bom OH added"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-bom-oh-details/{bom_id}/{process_id}")
def GetAllBomOHDetails(bom_id: int, process_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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

                data = db.query(models.BOM_OH_DETAILS, models.BOM.bom_name, models.PROCESS.process_name).join(models.PROCESS, models.PROCESS.id == models.BOM_OH_DETAILS.process_id).join(
                    models.BOM, models.BOM.id == models.PROCESS.bom_id).filter(models.BOM_OH_DETAILS.bom_id == bom_id, models.BOM_OH_DETAILS.process_id == process_id)
                return (u._asdict() for u in data.all())

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-bom-oh-details-by-ids/{ids}")
def GetBomOHDetailsByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                get_sc = db.query(models.BOM_OH_DETAILS.id, models.BOM_OH_DETAILS.overhead, models.BOM_OH_DETAILS.oh_bom, models.BOM_OH_DETAILS.oh_quantity, models.BOM_OH_DETAILS.oh_rate, models.BOM_OH_DETAILS.created_by,
                                  models.BOM_OH_DETAILS.created_on, models.BOM_OH_DETAILS.modified_by, models.BOM_OH_DETAILS.modified_on, models.PROCESS.process_name, models.BOM.bom_name).join(
                    models.PROCESS, models.PROCESS.id == models.BOM_OH_DETAILS.process_id
                ).join(models.BOM, models.BOM.id == models.PROCESS.bom_id).filter(models.BOM_OH_DETAILS.id == ids)

                return (get_sc.first()._asdict())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.put("/update-bom-oh-details/{ids}")
def UpdateBomOHDetails(ids: int, bom_oh_fields: schemas.BoMOHUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                bom_oh_fields_dict = bom_oh_fields.dict()
                bom_oh_fields_dict.update({"oh_cost": bom_oh_fields.oh_rate * bom_oh_fields.oh_quantity})

                db.query(models.BOM_OH_DETAILS).filter(
                    models.BOM_OH_DETAILS.id == ids).update(bom_oh_fields_dict)
                db.commit()
                return {"bom OH fields are updated!"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.delete("/delete-bom-oh-details/{ids}")
def DeleteBomOHDetails(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
            get_data = db.query(models.BOM_OH_DETAILS).filter(
                models.BOM_OH_DETAILS.id == ids)

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
