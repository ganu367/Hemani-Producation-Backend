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

router = APIRouter(prefix="/overhead", tags=["Overhead"])

get_db = database.get_db


@router.post("/create-overhead")
def CreateOverhead(overhead_fields: schemas.OHCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    company_id = current_user_login.user["companyID"]
    current_username = current_user_login.user["username"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            new_oh = models.OH(
                **overhead_fields.dict(), company_id=company_id)
            db.add(new_oh)
            db.commit()
            db.refresh(new_oh)

            return {"New overhead added"}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/shows-overhead")
def ShowOverhead(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            return db.query(models.OH).all()

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")
