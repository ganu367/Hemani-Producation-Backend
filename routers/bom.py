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

router = APIRouter(prefix="/bom", tags=["BOM"])

get_db = database.get_db


@router.post("/create-bom")
def createBom(bom_fields: schemas.BOMCreate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to create bom")
        else:
            try:
                bom_fields_dict = bom_fields.dict()
                del bom_fields_dict["process"]

                new_bom = models.BOM(
                    **bom_fields_dict)

                process_list = []

                for i in bom_fields.process:
                    process_list.append(models.PROCESS(**i.dict()))

                new_bom.process = process_list

                db.add(new_bom)
                db.commit()
                db.refresh(new_bom)

                return {"New BOM added"}
                # return new_bom

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-bom")
def GetAllBOM(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to create BoM")
        else:
            try:
                # data = db.query(models.StockMaster.item_name,  models.BOM.id, models.BOM.bom_name, models.BOM.bom_quantity, models.BOM.stock_id, models.BOM.uom, models.BOM.created_by, models.BOM.created_on, models.BOM.modified_by, models.BOM.modified_on,func.count(models.PROCESS.id).label("total_process")).join(
                #     models.BOM, models.BOM.stock_id == models.StockMaster.id)
                data = db.query(models.StockMaster.item_name,  models.BOM.id, models.BOM.bom_name, models.BOM.bom_quantity, models.BOM.stock_id, models.BOM.uom, models.BOM.created_by, models.BOM.created_on, models.BOM.modified_by, models.BOM.modified_on, func.count(models.PROCESS.id).label("total_process")).select_from(models.BOM
                                                                                                                                                                                                                                                                                                                                 ).outerjoin(models.PROCESS).outerjoin(models.StockMaster).group_by(models.PROCESS.bom_id)

                return (u._asdict() for u in data.all())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-bom-by-ids/{ids}")
def GetBOMByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to view BoM")
        else:
            # try:
                # get_sc = db.query(models.StockMaster.item_name,  models.BOM.id, models.BOM.bom_name, models.BOM.bom_quantity, models.BOM.stock_id, models.BOM.uom, models.BOM.created_by, models.BOM.created_on, models.BOM.modified_by, models.BOM.modified_on).join(
                #     models.BOM, models.BOM.stock_id == models.StockMaster.id).filter(models.BOM.id == ids)
                # get_sc = db.query(models.StockMaster.item_name, models.BOM, models.PROCESS).select_from(models.StockMaster).outerjoin(
                #     models.BOM).outerjoin(models.PROCESS).filter(models.BOM.id == ids)
                # return (u._asdict() for u in get_sc.all())
                get_bom = db.query(models.StockMaster.item_name, models.BOM).select_from(models.StockMaster).filter(models.BOM.id == ids).first()
                get_process = db.query(models.PROCESS).filter(models.PROCESS.bom_id == get_bom.BOM.id).all()
                return {"BOM": get_bom._asdict(), "PROCESS": get_process}
                # return (get_sc.first()._asdict())

            # except Exception as e:
            #     db.rollback()
            #     raise HTTPException(status_code=status.HTTP_302_FOUND,
            #                         detail=f"{str(e.orig)}")


@router.put("/update-bom/{ids}")
def UpdateBOM(ids: int, bom_fields: schemas.BOMUpdate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                                detail="You don't have permmission to update BoM")
        else:
            try:
                # db.query(models.BOM).filter(
                #     models.BOM.id == ids).update(bom_fields.dict())
                # db.commit()

                bom_fields_dict = bom_fields.dict()
                # process =  bom_fields_dict
                del bom_fields_dict["process"]

                new_bom = db.query(models.BOM).filter(
                    models.BOM.id == ids).update(bom_fields_dict)

                # bom = db.query(models.BOM).filter(
                #     models.BOM.id == ids)

                # process_list = []

                # for i in bom_fields.process:
                #     process_list.append(models.PROCESS(**i.dict()))

                # bom.process = process_list

                # db.add(bom)
                for i in bom_fields.process:
                    p1 = i.dict()
                    p1["bom_id"] = ids
                    process = models.PROCESS(**p1)
                    db.add(process)

                db.commit()

                return {"BoM fields are updated!"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.delete("/delete-bom/{ids}")
def DeleteBOM(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You don't have permmission to delete BoM")
        else:
            get_bom = db.query(models.BOM).filter(
                models.BOM.id == ids)

            if not get_bom.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="BOM data not found")
            else:
                # try:
                    get_process = db.query(models.PROCESS).filter(
                        models.PROCESS.bom_id == ids)
                    get_bom_stock = db.query(models.BOM_STOCK_DETAILS).filter(
                        models.BOM_STOCK_DETAILS.bom_id == ids)
                    get_bom_oh = db.query(models.BOM_OH_DETAILS).filter(
                        models.BOM_OH_DETAILS.bom_id == ids)

                    # count the child table
                    if (get_process.count() == 0 and get_bom_stock.count() == 0 and get_bom_oh.count() == 0):
                        db.query(models.BOM).filter(
                            models.BOM.id == ids).delete()
                        db.commit()
                        return{f"BOM is deleted"}

                    else:

                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f"ddelete related records: Process:{get_process.count()},Bom stock:{get_bom_stock.count()},Bom OH: {get_bom_oh.count()}...")

                # except Exception as error:
                #     db.rollback()
                #     raise HTTPException(status_code=status.HTTP_302_FOUND,
                #                         detail=f"{str(error.orig)}")
