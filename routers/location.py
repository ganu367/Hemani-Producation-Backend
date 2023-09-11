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

router = APIRouter(prefix="/location", tags=["Location"])

get_db = database.get_db


@router.post("/create-location")
def createLocation(location_fields: schemas.LocationCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            new_location = models.Location(
                **location_fields.dict())
            db.add(new_location)
            db.commit()
            db.refresh(new_location)

            return {f"location is created"}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-all-location")
def getAllLocation(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            get_location = db.query(models.Location.id,
                                    models.Location.location_name,
                                    models.Location.location_code,
                                    models.Location.created_by,
                                    models.Location.created_on,
                                    models.Location.modified_by,
                                    models.Location.modified_on,
                                    models.Plants.plant_name,
                                    models.Branch.branch_name,
                                    models.Company.company_name).join(models.Plants, models.Plants.id == models.Location.plant_id).join(models.Branch, models.Branch.id == models.Plants.branch_id).join(
                models.Company, models.Company.id == models.Branch.company_id)

            return (u._asdict() for u in get_location.all())

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-by-location-ids/{ids}")
def getByLocationIDs(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:

            get_location = db.query(models.Location, models.Plants.plant_name, models.Branch.branch_name, models.Company.company_name).join(models.Plants, models.Plants.id == models.Location.plant_id).join(models.Branch, models.Branch.id == models.Plants.branch_id).join(
                models.Company, models.Company.id == models.Branch.company_id).filter(
                models.Location.id == ids)

            if not get_location.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Location data not found")
            else:
                return (get_location.first()._asdict())

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.put("/update-location/{ids}")
def updateLocation(ids: int, location_fields: schemas.LocationUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        # try:
            get_location = db.query(models.Location).filter(
                models.Location.id == ids)

            if not get_location.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="branch data not found")
            else:

                location_fields_dict = location_fields.dict()
                # location_fields_dict.update(
                #     {"modified_by": current_username})

                db.query(models.Location).filter(models.Location.id == ids).update(
                    location_fields_dict)

                db.commit()
                return {f"location is updated"}

        # except Exception as error:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_302_FOUND,
        #                         detail=f"{str(error.orig)}")


@router.delete("/delete-location/{ids}")
def deleteLocation(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:

        get_location = db.query(models.Location).filter(
            models.Location.id == ids)

        if not get_location.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This plant data not found")
        else:
            # get_location.update({"is_deleted": True, "location_name": "del_"+str(
            #     ids)+"_"+get_location.first().location_name, "location_code": "del_"+str(ids)+"_"+get_location.first().location_code})
            # db.commit()
            # return{f"Location is deleted"}

            try:

                child_data = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                    models.BATCH_ACTUAL_CONSUMPTION.location_id == ids)

                if (child_data.count() == 0):

                    db.query(models.Location).filter(
                        models.Location.id == ids).delete()
                    db.commit()
                    return{f"Location is deleted"}

                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"delete related records {child_data.count()}")

            except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")
