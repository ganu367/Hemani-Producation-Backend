from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, asc
import database
import schemas
import models
import oauth2
from datetime import datetime
import pytz

current_date = datetime.now()
utc = pytz.UTC
router = APIRouter(prefix="/batch-actual-consumption",
                   tags=["Batch Actual Consumption"])

get_db = database.get_db


@router.post("/create-batch-ack-consumption")
def CreateBatchAckConsmuption(batch_ack_fields: schemas.BatchActualConsCreateList = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]
    user_plantID = current_user_login.user["plantID"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to create batch actual consumption")
        else:
            try:
                for k in batch_ack_fields.stock_details:

                    get_count = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                        models.BATCH_ACTUAL_CONSUMPTION.plant_id == user_plantID)
                    if get_count.count() == 0:
                        batch_ack_number = 1
                    else:
                        last_id = db.query(func.max(models.BATCH_ACTUAL_CONSUMPTION.batch_actual_number_id)).filter(
                            models.BATCH_ACTUAL_CONSUMPTION.plant_id == user_plantID).first()

                        batch_ack_number = int(last_id[0]) + 1

                    get_actual_cost = db.query(models.ActualCost).filter(
                        models.ActualCost.stock_id == k.stock_id).order_by(asc(models.ActualCost.from_date))

                    get_standard_cost = db.query(models.StandardCost).filter(
                        models.StandardCost.stock_id == k.stock_id).order_by(asc(models.StandardCost.from_date))

                    if k.in_out == "in":

                        if (get_actual_cost.count() == 0):
                            actual_rate = 0
                        else:
                            actual_rate = 0
                            for i in get_actual_cost.all():
                                if k.entry_date >= utc.localize(i.from_date):
                                    actual_rate = i.rate
                                else:
                                    break

                        if (get_standard_cost.count() == 0):
                            standard_rate = 0
                        else:
                            standard_rate = 0
                            for i in get_standard_cost.all():
                                if k.entry_date >= utc.localize(i.from_date):
                                    standard_rate = i.rate
                                else:
                                    break

                    else:
                        actual_rate = None
                        standard_rate = None

                    new_batch_ack_consump = models.BATCH_ACTUAL_CONSUMPTION(
                        **k.dict(), entry_number=str(user_plantID)+"_"+str(batch_ack_number), batch_actual_number_id=batch_ack_number, actual_rate=actual_rate, standard_rate=standard_rate, plant_id=user_plantID)

                    db.add(new_batch_ack_consump)
                db.commit()
                db.refresh(new_batch_ack_consump)

                return {"New batch actual consumption created"}

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-batch-ack-consumption")
def GetAllBatchAckConsumption(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to view all batch Actual Consumtpion")
        else:
            try:
                data = db.query(models.BATCH_ACTUAL_CONSUMPTION, models.BATCH.batch_number, models.PROCESS.process_name, models.StockMaster.item_name, models.StockMaster.uom, models.Plants.plant_name, models.Location.location_name
                                ).join(
                    models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id
                ).join(
                    models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_CONSUMPTION.process_id
                ).join(
                    models.StockMaster, models.StockMaster.id == models.BATCH_ACTUAL_CONSUMPTION.stock_id
                ).join(
                    models.Plants, models.Plants.id == models.BATCH_ACTUAL_CONSUMPTION.plant_id
                ).join(
                    models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id)

                return (u._asdict() for u in data.all())

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-all-batch-ack-consumption-entries")
def GetAllBatchAckConsumptionEntries(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to view all batch Actual Consumtpion")
        else:
            try:
                data = db.query(models.BATCH_ACTUAL_CONSUMPTION, models.BATCH.batch_number, models.PROCESS.process_name, models.StockMaster.item_name, models.StockMaster.uom, models.Plants.plant_name, models.Location.location_name
                                ).join(
                    models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id
                ).join(
                    models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_CONSUMPTION.process_id
                ).join(
                    models.StockMaster, models.StockMaster.id == models.BATCH_ACTUAL_CONSUMPTION.stock_id
                ).join(
                    models.Plants, models.Plants.id == models.BATCH_ACTUAL_CONSUMPTION.plant_id
                ).join(
                    models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id
                ).group_by(
                    models.BATCH_ACTUAL_CONSUMPTION.entry_number)

                return (u._asdict() for u in data.all())

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.get("/get-batch-ack-consumption-by-ids/{entry}")
def GetBatchAckConsumptionByIds(entry: str, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to view Process")
        else:

            try:
                get_sc = db.query(models.BATCH_ACTUAL_CONSUMPTION, models.BATCH, models.PROCESS, models.Plants, models.StockMaster, models.Location
                                  ).join(
                    models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id
                ).join(
                    models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_CONSUMPTION.process_id
                ).join(
                    models.StockMaster, models.StockMaster.id == models.BATCH_ACTUAL_CONSUMPTION.stock_id
                ).join(
                    models.Plants, models.Plants.id == models.BATCH_ACTUAL_CONSUMPTION.plant_id
                ).join(
                    models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id
                ).filter(models.BATCH_ACTUAL_CONSUMPTION.entry_number == entry)

                return (u._asdict() for u in get_sc.all())

                # return (get_sc.first()._asdict())
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")


@router.put("/update-batch-ack-consumption/{ids}")
def UpdateBatchAckConsumption(ids: int, batch_ack_fields: schemas.BatchActualConsUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
                                detail="You don't have permmission to update Batch Actual Consumption")
        else:
            get_batch_ack = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                models.BATCH_ACTUAL_CONSUMPTION.id == ids)
            if get_batch_ack.first():
                try:

                    get_actual_cost = db.query(models.ActualCost).filter(
                        models.ActualCost.stock_id == get_batch_ack.first().stock_id).order_by(asc(models.ActualCost.from_date))

                    get_standard_cost = db.query(models.StandardCost).filter(
                        models.StandardCost.stock_id == get_batch_ack.first().stock_id).order_by(asc(models.StandardCost.from_date))

                    if batch_ack_fields.in_out == "in":

                        if (get_actual_cost.count() == 0):
                            actual_rate = 0
                        else:
                            actual_rate = 0
                            for i in get_actual_cost.all():
                                if batch_ack_fields.entry_date >= utc.localize(i.from_date):
                                    actual_rate = i.rate
                                else:
                                    break

                        if (get_standard_cost.count() == 0):
                            standard_rate = 0
                        else:
                            standard_rate = 0
                            for i in get_standard_cost.all():
                                if batch_ack_fields.entry_date >= utc.localize(i.from_date):
                                    standard_rate = i.rate
                                else:
                                    break

                    else:
                        actual_rate = None
                        standard_rate = None

                    batch_ack_fields_dict = batch_ack_fields.dict()
                    batch_ack_fields_dict.update(
                        {"actual_rate": actual_rate, "standard_rate": standard_rate})

                    db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                        models.BATCH_ACTUAL_CONSUMPTION.id == ids).update(batch_ack_fields_dict)
                    db.commit()
                    return {"Batch Actual Consumption fields are updated!"}

                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(e.orig)}")
            else:
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"Batch Actual Consumption not found")


@router.delete("/delete-batch-ack-consumption/{ids}")
def DeleteBatchAckConsumption(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to delete Batch Actual Consumption ")
        else:
            get_data = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                models.BATCH_ACTUAL_CONSUMPTION.id == ids)

            if not get_data.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Batch Actual Consumption  data not found")
            else:
                try:
                    db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                        models.BATCH_ACTUAL_CONSUMPTION.id == ids).delete()
                    db.commit()
                    return{f"Batch Actual Consumption is deleted"}

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")


@router.delete("/delete-batch-ack-consumption-entries/{entry}")
def DeleteBatchAckConsumption(entry: str, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    user_role = current_user_login.user["role"]

    if not (isAdmin_user == False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="not authenticated")
    else:
        if not (user_role == "Production Executive"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You don't have permmission to delete Batch Actual Consumption ")
        else:
            get_data = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                models.BATCH_ACTUAL_CONSUMPTION.entry_number == entry)

            if not get_data.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Batch Actual Consumption  data not found")
            else:
                try:
                    db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
                        models.BATCH_ACTUAL_CONSUMPTION.entry_number == entry).delete()
                    db.commit()
                    return{f"Batch Actual Consumption is deleted"}

                except Exception as error:
                    db.rollback()
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                        detail=f"{str(error.orig)}")
