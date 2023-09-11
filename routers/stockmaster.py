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

router = APIRouter(prefix="/stock", tags=["StockMaster"])

get_db = database.get_db


@router.post("/create-stock")
def createStock(stock_fields: schemas.StockMasterCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]
    current_plantID = current_user_login.user["plantID"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            get_plant = db.query(models.Plants).filter(
                models.Plants.id == current_plantID)

            new_stock = models.StockMaster(
                **stock_fields.dict(), company_id=get_plant.first().company_id)
            db.add(new_stock)
            db.commit()
            db.refresh(new_stock)

            return {"New stock added"}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-all-stock")
def getAllStock(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        company_id = current_user_login.user["companyID"]
        stock_data = db.query(models.StockMaster).filter(
            models.StockMaster.company_id == company_id).all()
        return stock_data


@router.get("/get-by-stock-ids/{ID}")
def getByStockIDs(ID: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        stock_data = db.query(models.StockMaster).filter(
            models.StockMaster.id == ID).first()
        return stock_data


@router.put("/update-stock/{ids}")
def updateStock(ids: int, stock_fields: schemas.StockMasterUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:

        try:

            db.query(models.StockMaster).filter(models.StockMaster.id == ids).update(
                stock_fields.dict())
            db.commit()

            return {"Successfully Updated stock fields"}

        except Exception as error:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(error.orig)}")


@router.delete("/delete-stock/{stock_id}")
def deleteStcok(stock_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        get_stock = db.query(models.StockMaster).filter(
            models.StockMaster.id == stock_id)

        if not get_stock.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="stock data not found")
        else:
            try:

                # count the child table
                child_data = db.query(models.StandardCost).filter(
                    models.StandardCost.stock_id == stock_id)

                if (child_data.count() == 0):
                    db.query(models.StockMaster).filter(
                        models.StockMaster.id == stock_id).delete()
                    db.commit()
                    return{f"Stock Master is deleted"}

                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                                detail=f"delete related records {child_data.count()}")
            except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")
