from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
import database
import schemas
import models
import oauth2
from typing import List, Optional
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

router = APIRouter(prefix="/plant", tags=["Plants"])

get_db = database.get_db


@router.post("/create-plant")
def createPlant(plant_fields: schemas.PlantCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            new_plant = models.Plants(
                **plant_fields.dict())
            db.add(new_plant)
            db.commit()
            db.refresh(new_plant)

            return {f"Plant is created"}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-all-plant")
def getAllPlant(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            get_plant = db.query(models.Plants.id,
                                 models.Plants.plant_name,
                                 models.Plants.plant_code,
                                 models.Plants.created_by,
                                 models.Plants.created_on,
                                 models.Plants.modified_by,
                                 models.Plants.modified_on,
                                 models.Branch.branch_name,
                                 models.Company.company_name).join(models.Branch, models.Branch.id == models.Plants.branch_id).join(
                models.Company, models.Company.id == models.Branch.company_id)

            return (u._asdict() for u in get_plant.all())

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-by-plant-ids/{ids}")
def getByPlantIDs(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        # try:

            # get_plant = db.query(models.Plants).filter(
            #     models.Plants.id == ids)

            get_plant = db.query(models.Plants, models.Branch.branch_name, models.Company.company_name).join(models.Branch, models.Branch.id == models.Plants.branch_id).join(
                models.Company, models.Company.id == models.Branch.company_id).filter(models.Plants.id == ids)
            print(get_plant.first())
            if not get_plant.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Plant data not found")
            else:
                return (get_plant.first()._asdict())

        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_302_FOUND,
        #                         detail=f"{str(e.orig)}")


@router.put("/update-plant/{ids}")
def updatePlant(ids: int, plant_fields: schemas.PlantUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            get_plant = db.query(models.Plants).filter(
                models.Plants.id == ids)

            if not get_plant.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="branch data not found")
            else:

                plant_fields_dict = plant_fields.dict()
                # plant_fields_dict.update(
                #     {"modified_by": current_username})

                db.query(models.Plants).filter(models.Plants.id == ids).update(
                    plant_fields_dict)

                db.commit()
            return {f"Plant is updated"}

        except Exception as error:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(error.orig)}")


@router.delete("/delete-plant/{ids}")
def deletePlant(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        get_plant = db.query(models.Plants).filter(
            models.Plants.id == ids)

        if not get_plant.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This plant data not found")
        else:

            try:

                # count the child table
                child_data = db.query(models.Location).filter(
                    models.Location.plant_id == ids)
                get_batch_data = db.query(models.BATCH).filter(
                    models.BATCH.plant_id == ids)

                get_batch_actual_con = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                    models.BATCH_ACTUAL_CONSUMPTION.plant_id == ids)

                get_batch_actual_oh = db.query(models.BATCH_ACTUAL_OH).filter(
                    models.BATCH_ACTUAL_OH.plant_id == ids)

                if (child_data.count() == 0, get_batch_data.count() == 0, get_batch_actual_con.count() == 0, get_batch_actual_oh.count() == 0):

                    db.query(models.Plants).filter(
                        models.Plants.id == ids).delete()
                    db.commit()
                    return{f"Plants is deleted"}

                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"delete related records {child_data.count()},Batch:{get_batch_data.count()},Batch Actual Con:{get_batch_actual_con.count()},Batch Actual OH: {get_batch_actual_oh.count()}")

            except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")
