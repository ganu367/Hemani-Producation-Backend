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

router = APIRouter(prefix="/branch", tags=["Branch"])

get_db = database.get_db


@router.post("/create-branch")
def createBranch(branch_fields: schemas.BranchCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            new_branch = models.Branch(
                **branch_fields.dict())
            db.add(new_branch)
            db.commit()
            db.refresh(new_branch)

            return {f"Branch is created"}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-all-branches")
def getAllBranches(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:

            get_branch = db.query(models.Branch.id,
                                  models.Branch.branch_name,
                                  models.Branch.branch_code,
                                  models.Branch.gst_number,
                                  models.Branch.pan_number,
                                  models.Branch.address,
                                  models.Branch.created_by,
                                  models.Branch.created_on,
                                  models.Branch.modified_by,
                                  models.Branch.modified_on,
                                  models.Company.company_name).join(
                models.Company, models.Company.id == models.Branch.company_id)

            return (u._asdict() for u in get_branch.all())

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-branches-by-id/{ids}")
def getBranchesByIDs(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:

            get_branch = db.query(models.Branch, models.Company.company_name).join(
                models.Company, models.Company.id == models.Branch.company_id).filter(models.Branch.id == ids)

            if not get_branch.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="This branch data not found")
            else:
                return (get_branch.first()._asdict())

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.put("/update-branch/{ids}")
def updateBranch(ids: int, branch_fields: schemas.BranchUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            get_branch = db.query(models.Branch).filter(
                models.Branch.id == ids)

            if not get_branch.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="branch data not found")
            else:

                branch_fields_dict = branch_fields.dict()
                # branch_fields_dict.update(
                #     {"modified_by": current_username})

                db.query(models.Branch).filter(models.Branch.id == ids).update(
                    branch_fields_dict)

                db.commit()
                return {f"Branch is updated"}

        except Exception as error:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(error.orig)}")


@router.delete("/delete-branch/{ids}")
def deleteBranch(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        get_branch = db.query(models.Branch).filter(
            models.Branch.id == ids)

        if not get_branch.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="This branch data not found")
        else:

            try:
                # count the child table
                child_data = db.query(models.Plants).filter(
                    models.Plants.branch_id == ids)

                if (child_data.count() == 0):

                    db.query(models.Branch).filter(
                        models.Branch.id == ids).delete()
                    db.commit()
                    return{f"Branch is deleted"}

                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f"delete related records {child_data.count()}")
            except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")
