from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, asc
from sqlalchemy.orm import Session
import database
import models
from os import getcwd, remove
import base64
import os
from datetime import datetime

router = APIRouter(prefix="/api/utility", tags=["Utility"])

get_db = database.get_db


@router.get("/send-file")
def sendFile(file_path: str):
    if os.path.exists(str(file_path)):

        with open(file_path, mode="rb") as image_file:
            image_string = base64.b64encode(image_file.read())
            return image_string
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found")


def actualRate(stock_id: int, entry_date: datetime, db: Session = Depends(get_db)):
    get_actual_cost = db.query(models.ActualCost).filter(
        models.ActualCost.stock_id == stock_id).order_by(asc(models.ActualCost.from_date))

    if (get_actual_cost.count() == 0):
        actual_rate = 0
    else:
        actual_rate = 0
        for i in get_actual_cost.all():
            if entry_date >= i.from_date:
                actual_rate = i.rate
            else:
                break
    return actual_rate


def standardRate(stock_id: int, entry_date: datetime, db: Session = Depends(get_db)):

    get_standard_cost = db.query(models.StandardCost).filter(
        models.StandardCost.stock_id == stock_id).order_by(asc(models.StandardCost.from_date))

    if (get_standard_cost.count() == 0):
        standard_rate = 0
    else:
        standard_rate = 0
        for i in get_standard_cost.all():
            if entry_date >= i.from_date:
                standard_rate = i.rate
            else:
                break
    return standard_rate


def actualOverheadCost(batch_id: int, db: Session = Depends(get_db)):
    if not db.query(models.BATCH_ACTUAL_OH).filter(models.BATCH_ACTUAL_OH.batch_id == batch_id).first():
        return 0
    else:
        get_batch_actual_oh = db.query(func.sum(models.BATCH_ACTUAL_OH.oh_cost)).filter(
            models.BATCH_ACTUAL_OH.batch_id == batch_id)

        return get_batch_actual_oh.first()[0]


def actualCostRawMaterail(batch_id: int, db: Session = Depends(get_db)):
    get_batch_actual_cons = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
        models.BATCH_ACTUAL_CONSUMPTION.in_out == "in", models.BATCH_ACTUAL_CONSUMPTION.batch_id == batch_id)
    actual_rate = 0
    actual_cost = 0
    for i in get_batch_actual_cons.all():
        actual_rate = actualRate(i.stock_id, i.entry_date, db)
        cost = actual_rate*i.quantity
        actual_cost = actual_cost + cost
    return actual_cost


def standardOverheadCost(bom_id: int, db: Session = Depends(get_db)):
    if not db.query(models.BOM_OH_DETAILS).filter(models.BOM_OH_DETAILS.bom_id == bom_id).first():
        return 0
    else:
        get_standard_oh = db.query(func.sum(models.BOM_OH_DETAILS.oh_cost)).filter(
            models.BOM_OH_DETAILS.bom_id == bom_id)

        return get_standard_oh.first()[0]


def standardCostRawMaterail(bom_id: int, end_date: datetime, db: Session = Depends(get_db)):
    get_bom_stock_details = db.query(models.BOM_STOCK_DETAILS).filter(
        models.BOM_STOCK_DETAILS.in_out == "in", models.BOM_STOCK_DETAILS.bom_id == bom_id)
    
    standard_rate = 0
    standard_cost = 0
    for i in get_bom_stock_details.all():
        standard_rate = standardRate(i.stock_id, end_date, db)
        cost = standard_rate*i.bom_quantity
        standard_cost = standard_cost + cost
    
    return standard_cost


def deleteFile(file_path: str):
    if os.path.exists(str(file_path)):
        remove(str(file_path))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
