from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, or_, and_
import database
import schemas
import models
import oauth2
from routers.utility import actualCostRawMaterail, actualOverheadCost, standardCostRawMaterail, standardOverheadCost
from datetime import datetime
import json
from .utility import actualRate, standardRate
import pandas as pd
import numpy as np
import pytz

utc = pytz.UTC
current_date = datetime.now()

router = APIRouter(prefix="/api", tags=["Options"])

get_db = database.get_db


@router.get("/get-company")
def getCompany(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        comapny_data = db.query(
            models.Company.id, models.Company.company_name)

        return (u._asdict() for u in comapny_data.all())


@router.get("/get-branch/{cid}")
def getBranch(cid: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        branch_data = db.query(
            models.Branch.id, models.Branch.branch_name).filter(models.Branch.company_id == cid)
        return (u._asdict() for u in branch_data.all())


@router.get("/get-plant/{bid}")
def getPlant(bid: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        plants_data = db.query(
            models.Plants.id, models.Plants.plant_name).filter(models.Plants.branch_id == bid)

        return (u._asdict() for u in plants_data.all())


@router.get("/get-locations/{lid}")
def getLocation(lid: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        location_data = db.query(
            models.Location.id, models.Location.location_name).filter(models.Location.plant_id == lid)

        return (u._asdict() for u in location_data.all())


@router.get("/get-process/{bom_id}")
def getProcess(bom_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
            all_process_data = db.query(models.PROCESS.id, models.PROCESS.process_name).filter(
                models.PROCESS.bom_id == bom_id)

            return (u._asdict() for u in all_process_data.all())


@router.get("/get-processes-for-batch/{batch_id}")
def getProcessesForBatch(batch_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
            all_data = db.query(models.PROCESS).select_from(models.BATCH).join(models.BOM, models.BOM.id == models.BATCH.bom_id).join(models.PROCESS, models.PROCESS.bom_id == models.BOM.id).filter(models.BATCH.id == batch_id)
            
            return (all_data.all())


@router.get("/get-bom/{stock_id}")
def getBOM(stock_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
            all_data = db.query(models.BOM.id, models.BOM.bom_name).filter(
                models.BOM.stock_id == stock_id)
            return (u._asdict() for u in all_data.all())


@router.get("/show-batches-for-stock/{stock_id}")
def ShowBatchesForStock(stock_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    user_plantID = current_user_login.user["plantID"]

    get_batch = db.query(models.BATCH).filter(models.BATCH.status == "open",
                                              models.BATCH.stock_id == stock_id, models.BATCH.plant_id == user_plantID)
    return get_batch.all()


@router.get("/show-stock-with-batches")
def ShowStockWithBatches(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    user_plantID = current_user_login.user["plantID"]

    get_batch = db.query(models.StockMaster.id, models.StockMaster.item_name).select_from(models.BATCH).join(
        models.StockMaster).group_by(models.BATCH.stock_id).filter(models.BATCH.status == "open")
    return (u._asdict() for u in get_batch.all())


@router.get("/get-locations-for-user-plant")
def GetLocationsForUserPlant(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    user_plantID = current_user_login.user["plantID"]

    get_batch = db.query(models.Location).filter(
        models.Location.plant_id == user_plantID)

    return (get_batch.all())


@router.get("/get-stock-for-{in_out}")
def getStockForInOut(in_out: str, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
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
            if (in_out == "in"):
                all_data = db.query(models.StockMaster).filter(
                    or_(models.StockMaster.item_category == "Raw Material", models.StockMaster.item_category == "Work in Progress"))
            else:
                all_data = db.query(models.StockMaster).filter(
                    or_(models.StockMaster.item_category == "Finished Goods", models.StockMaster.item_category == "Work in Progress"))
            return (all_data.all())


@router.get("/get-finished-goods")
def getStockForInOut(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    # isAdmin_user = current_user_login.user["isAdmin"]
    # user_role = current_user_login.user["role"]

    # if not (isAdmin_user == False):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="not authenticated")
    # else:
    #     if not (user_role == "Production Executive"):
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail="You don't have permmission to view Process")
    #     else:
    all_data = db.query(models.StockMaster).filter(
        models.StockMaster.item_category == "Finished Goods")

    return (all_data.all())


@router.get("/show-closed-batches-for-stock/{stock_id}")
def ShowClosedBatchesForStock(stock_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    user_plantID = current_user_login.user["plantID"]

    get_batch = db.query(models.BATCH).filter(models.BATCH.status == "closed",
                                              models.BATCH.stock_id == stock_id, models.BATCH.plant_id == user_plantID)
    return get_batch.all()


# Report api below
@router.get("/all-show-batch")
def ShowBatch(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    get_batch = db.query(models.BATCH).filter(models.BATCH.status == "closed")
    return get_batch.all()


@router.get("/all-generate-report/{stock_id}/{batch_id}")
def GenerateReports(batch_id: int, stock_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    # user_role = current_user_login.user["role"]
    # if not (isAdmin_user == False):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="not authenticated")
    # else:
    #     if not (user_role == "Production Executive"):
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail="You don't have permmission to view Process")
    #     else:

    if not db.query(models.BATCH).filter(models.BATCH.status == "closed", models.BATCH.stock_id == stock_id, models.BATCH.id == batch_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="records not found")
    else:
        try:
            # batch details goes here
            get_batch = db.query(models.BATCH.batch_number, models.BATCH.start_date, models.BATCH.end_date, models.BATCH.batch_quantity, models.BATCH.bom_id, models.BOM.bom_name, models.StockMaster.item_name, models.Plants.plant_name).select_from(models.BATCH).outerjoin(models.BOM).outerjoin(models.StockMaster).outerjoin(
                models.Plants).filter(models.BATCH.status == "closed", models.BATCH.stock_id == stock_id, models.BATCH.id == batch_id)
            # bom stock detail goes here
            ############### batch actual in #############
            get_bom_stock_details = db.query(models.BOM_STOCK_DETAILS.stock_id, models.BOM_STOCK_DETAILS.uom, models.BOM_STOCK_DETAILS.process_id, models.BOM_STOCK_DETAILS.bom_quantity, models.StockMaster.item_name, models.StockMaster.item_code, models.PROCESS.process_name).select_from(
                models.BOM_STOCK_DETAILS).outerjoin(models.StockMaster).outerjoin(models.PROCESS).filter(models.BOM_STOCK_DETAILS.bom_id == get_batch.first().bom_id, models.BOM_STOCK_DETAILS.in_out == "in")



            # batch actual consumption code goes here
            get_consum_data = db.query(models.BATCH_ACTUAL_CONSUMPTION.entry_number, models.BATCH_ACTUAL_CONSUMPTION.entry_sr_number, models.BATCH_ACTUAL_CONSUMPTION.stock_id, models.BATCH_ACTUAL_CONSUMPTION.location_id, models.BATCH_ACTUAL_CONSUMPTION.batch_id, models.BATCH_ACTUAL_CONSUMPTION.process_id, models.BATCH_ACTUAL_CONSUMPTION.plant_id,
                                        models.BATCH_ACTUAL_CONSUMPTION.entry_date, models.BATCH_ACTUAL_CONSUMPTION.uom,
                                        models.BATCH_ACTUAL_CONSUMPTION.quantity, models.BATCH_ACTUAL_CONSUMPTION.in_out, models.StockMaster.item_name,
                                        models.StockMaster.item_code, models.Location.location_name, models.BATCH.batch_number, models.PROCESS.process_name, models.Plants.plant_name).select_from(models.BATCH_ACTUAL_CONSUMPTION).outerjoin(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id).outerjoin(models.StockMaster, models.StockMaster.id == models.BATCH_ACTUAL_CONSUMPTION.stock_id).outerjoin(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_CONSUMPTION.process_id).outerjoin(models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id).outerjoin(models.Plants, models.Plants.id == models.BATCH_ACTUAL_CONSUMPTION.plant_id).filter(models.BATCH_ACTUAL_CONSUMPTION.in_out == "in", models.BATCH_ACTUAL_CONSUMPTION.batch_id == batch_id)
            if (get_consum_data.count() != 0):
            # actual cost report
                get_consum_data_list = []
                for i in get_consum_data.all():
                    get_actual_rate = actualRate(
                        i.stock_id, i.entry_date, db)
                    get_standard_rate = standardRate(
                        i.stock_id, i.entry_date, db)
                    i1 = i._asdict()
                    if (get_actual_rate != None):
                        i1["actual_rate"] = get_actual_rate
                    else:
                        i1["actual_rate"] = 0
                    if (get_standard_rate != None):
                        i1["standard_rate"] = get_standard_rate
                    else:
                        i1["standard_rate"] = 0
                    get_consum_data_list.append(i1)

                df = pd.DataFrame.from_dict(get_consum_data_list)

                df['actual_cost'] = df['actual_rate'] * df['quantity']

                df_actual = df.groupby(['process_name', 'item_code', 'item_name', 'uom']).agg(
                    {'quantity': "sum", 'actual_cost': "sum"}).reset_index()

                # standard cost report
                get_standard_rate_list = []
                if (get_bom_stock_details.count() != 0):
                    for i in get_bom_stock_details.all():
                        get_standard_rate = standardRate(
                            i.stock_id, get_batch.first().end_date, db)
                        i1 = i._asdict()
                        i1["standard_rate"] = get_standard_rate
                        get_standard_rate_list.append(i1)

                    df = pd.DataFrame.from_dict(get_standard_rate_list)
                    df['stadard_cost'] = df['standard_rate'] * df['bom_quantity']

                    df_standard = df.groupby(['process_name', 'item_code', 'item_name', 'uom']).agg(
                        {'bom_quantity': "sum", 'stadard_cost': "sum"}).reset_index()
                else:
                    df_standard = pd.DataFrame(columns=['standard_rate', 'stadard_cost', 'bom_quantity', 'process_name', 'item_code', 'item_name', 'uom'])
                # merge two batch_actual_in and batch_actual_in DataFrame for in
                final_df = pd.merge(df_actual, df_standard, on=[
                                    'process_name', 'item_code', 'item_name', 'uom'], how='outer').fillna(0)

                final_df['quantity_variance'] = final_df['bom_quantity'] - \
                    final_df['quantity']
                final_df['cost_variance'] = final_df['stadard_cost'] - \
                    final_df['actual_cost']

                # final_df['avg_rate'] = final_df['actual_cost']/final_df['quantity']
                # final_df['std_rate'] = final_df['stadard_cost']/final_df['bom_quantity']
            else:
                get_standard_rate_list = []
                if (get_bom_stock_details.count() != 0):
                    for i in get_bom_stock_details.all():
                        get_standard_rate = standardRate(
                            i.stock_id, get_batch.first().end_date, db)
                        i1 = i._asdict()
                        i1["standard_rate"] = get_standard_rate
                        get_standard_rate_list.append(i1)

                    df = pd.DataFrame.from_dict(get_standard_rate_list)
                    df['stadard_cost'] = df['standard_rate'] * df['bom_quantity']

                    df_standard = df.groupby(['process_name', 'item_code', 'item_name', 'uom']).agg(
                        {'bom_quantity': "sum", 'stadard_cost': "sum"}).reset_index()
                else:
                    df_standard = pd.DataFrame(columns=['stock_id', 'item_code', 'item_name', 'uom', 'bom_quantity'])
        
                df_actual = pd.DataFrame(columns=['process_name', 'item_code', 'item_name', 'uom', 'quantity', 'actual_cost', 'stock_id'])
                final_df = pd.merge(df_actual, df_standard, on=[
                    'process_name', 'item_code', 'item_name', 'uom'], how='outer').fillna(0)
                
                final_df['quantity_variance'] = final_df['bom_quantity'] - \
                    final_df['quantity']
                final_df['cost_variance'] = final_df['stadard_cost'] - \
                    final_df['actual_cost']
                



            ############### batch actual out #############

            get_consum_data_out = db.query(models.BATCH_ACTUAL_CONSUMPTION.entry_number, models.BATCH_ACTUAL_CONSUMPTION.stock_id,
                                            models.BATCH_ACTUAL_CONSUMPTION.uom, models.BATCH_ACTUAL_CONSUMPTION.quantity, models.StockMaster.item_name,
                                            models.StockMaster.item_code, models.BATCH.batch_number).select_from(models.BATCH_ACTUAL_CONSUMPTION).outerjoin(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id).outerjoin(models.StockMaster, models.StockMaster.id == models.BATCH_ACTUAL_CONSUMPTION.stock_id).outerjoin(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_CONSUMPTION.process_id).outerjoin(models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id).outerjoin(models.Plants, models.Plants.id == models.BATCH_ACTUAL_CONSUMPTION.plant_id).filter(models.BATCH_ACTUAL_CONSUMPTION.in_out == "out", models.BATCH_ACTUAL_CONSUMPTION.batch_id == batch_id)
            get_bom_stock_details_out = db.query(models.BOM_STOCK_DETAILS.stock_id, models.BOM_STOCK_DETAILS.bom_quantity, models.BOM_STOCK_DETAILS.uom, models.StockMaster.item_name, models.StockMaster.item_code).select_from(
                models.BOM_STOCK_DETAILS).outerjoin(models.StockMaster).outerjoin(models.PROCESS).filter(models.BOM_STOCK_DETAILS.bom_id == get_batch.first().bom_id, models.BOM_STOCK_DETAILS.in_out == "out")
            if (get_consum_data_out.count() != 0):

                # batch_actual_out
                df_batch_actual = pd.DataFrame.from_dict(
                    get_consum_data_out)

                df_batch_actual = df_batch_actual.groupby(['stock_id', 'item_code', 'item_name', 'uom']).agg(
                    {'quantity': "sum"}).reset_index()

                # batch_standard_out
                if (get_bom_stock_details_out.count() != 0):

                    df_batch_standard = pd.DataFrame.from_dict(
                        get_bom_stock_details_out)

                    df_batch_standard = df_batch_standard.groupby(['stock_id', 'item_code', 'item_name', 'uom']).agg(
                        {'bom_quantity': "sum"}).reset_index()
                else:
                    df_batch_standard = pd.DataFrame(columns=['stock_id', 'item_code', 'item_name', 'uom', 'bom_quantity'])
                # merge two batch_actual_out and batch_standard_out DataFrame for out
                final_df_out = pd.merge(df_batch_actual, df_batch_standard, on=[
                    'stock_id', 'item_code', 'item_name', 'uom'], how='outer').fillna(0)
            else:
                if (get_bom_stock_details_out.count() != 0):

                    df_batch_standard = pd.DataFrame.from_dict(
                        get_bom_stock_details_out)

                    df_batch_standard = df_batch_standard.groupby(['stock_id', 'item_code', 'item_name', 'uom']).agg(
                        {'bom_quantity': "sum"}).reset_index()
                else:
                    df_batch_standard = pd.DataFrame(columns=['stock_id', 'item_code', 'item_name', 'uom', 'bom_quantity'])
        
                df_batch_actual = pd.DataFrame(columns=['entry_number', 'quantity', 'batch_number', 'stock_id', 'item_code', 'item_name', 'uom'])
                final_df_out = pd.merge(df_batch_actual, df_batch_standard, on=[
                    'stock_id', 'item_code', 'item_name', 'uom'], how='outer').fillna(0)
                




            ########################################## batch actual overhead #########################
            get_batch_actual_overhead = db.query(models.PROCESS.process_name, models.BATCH_ACTUAL_OH.overhead, models.BATCH_ACTUAL_OH.oh_uom, models.BATCH_ACTUAL_OH.oh_quantity, models.BATCH_ACTUAL_OH.oh_rate).select_from(
                models.BATCH_ACTUAL_OH).outerjoin(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_OH.batch_id).outerjoin(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_OH.process_id).filter(models.BATCH_ACTUAL_OH.batch_id == batch_id)

            get_bom_standard_oh = db.query(models.PROCESS.process_name, models.BOM_OH_DETAILS.overhead, models.BOM_OH_DETAILS.oh_uom, models.BOM_OH_DETAILS.oh_quantity.label("standard_quantity"), models.BOM_OH_DETAILS.oh_rate.label("standard_rate")).select_from(
                models.BOM_OH_DETAILS).outerjoin(models.PROCESS, models.PROCESS.id == models.BOM_OH_DETAILS.process_id).filter(models.BOM_OH_DETAILS.bom_id == get_batch.first().bom_id)
            if (get_batch_actual_overhead.count() != 0):

                df = pd.DataFrame.from_dict(get_batch_actual_overhead)

                df['oh_cost'] = df['oh_rate'] * df['oh_quantity']
                df_overhead_actual = df.groupby(['process_name', 'overhead', 'oh_uom']).agg(
                    {'oh_quantity': "sum", 'oh_cost': "sum"}).reset_index()

                # batch standard overhead
                if (get_bom_standard_oh.count() != 0):
                    df_standard_oh = pd.DataFrame().from_dict(get_bom_standard_oh)
                    df_standard_oh['oh_standard_cost'] = df_standard_oh['standard_rate'] * \
                        df_standard_oh['standard_quantity']

                    df_overhead_standard = df_standard_oh.groupby(['process_name', 'overhead', 'oh_uom']).agg(
                        {'standard_quantity': "sum", 'oh_standard_cost': "sum"}).reset_index()
                else:
                    df_overhead_standard = pd.DataFrame(columns=['oh_standard_cost', 'standard_rate', 'standard_quantity', 'process_name', 'overhead', 'oh_uom'])

                final_df_overhead = pd.merge(df_overhead_actual, df_overhead_standard, on=[
                    'process_name', 'overhead', 'oh_uom'], how='outer').fillna(0)

                final_df_overhead['quantity_variance'] = final_df_overhead['standard_quantity'] - \
                    final_df_overhead['oh_quantity']

                final_df_overhead['cost_variance'] = final_df_overhead['oh_standard_cost'] - \
                    final_df_overhead['oh_cost']
            else:
                if (get_bom_standard_oh.count() != 0):
                    df_standard_oh = pd.DataFrame().from_dict(get_bom_standard_oh)
                    df_standard_oh['oh_standard_cost'] = df_standard_oh['standard_rate'] * \
                        df_standard_oh['standard_quantity']

                    df_overhead_standard = df_standard_oh.groupby(['process_name', 'overhead', 'oh_uom']).agg(
                        {'standard_quantity': "sum", 'oh_standard_cost': "sum"}).reset_index()
                else:
                    df_overhead_standard = pd.DataFrame(columns=['oh_standard_cost', 'standard_rate', 'standard_quantity', 'process_name', 'overhead', 'oh_uom'])
                
                df_overhead_actual = pd.DataFrame(columns=['process_name', 'overhead', 'oh_uom', 'oh_quantity', 'oh_cost'])
                final_df_overhead = pd.merge(df_overhead_actual, df_overhead_standard, on=[
                    'process_name', 'overhead', 'oh_uom'], how='outer').fillna(0)
                
                final_df_overhead['quantity_variance'] = final_df_overhead['standard_quantity'] - \
                    final_df_overhead['oh_quantity']

                final_df_overhead['cost_variance'] = final_df_overhead['oh_standard_cost'] - \
                    final_df_overhead['oh_cost']




            return {"Basic": (u._asdict() for u in get_batch.all()), "Consumpation_data": (x._asdict() for x in get_consum_data.all()), "consumption": final_df.to_json(orient='records'), "consumption_out": final_df_out.to_json(orient='records'), "overhead_reports": final_df_overhead.to_json(orient='records')}

        # except Exception as error:
        #     db.rollback()
        #     raise HTTPException(status_code=status.HTTP_302_FOUND,
        #                         detail=f"{str(error.orig)}")
        finally:
            df = pd.DataFrame()
            del df


@router.post("/generate-report-for-stock-wise")
def GenerateReportsStockWise(dates: schemas.GenerateReportsStockWise = Body(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    # user_role = current_user_login.user["role"]

    # if not (isAdmin_user == False):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="not authenticated")
    # else:
    #     if not (user_role == "Production Executive"):
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail="You don't have permmission to view Process")
    #     else:
    from_date = dates.from_date
    to_date = dates.to_date

    try:
                # batch  goes here
                get_batch = db.query(models.BATCH.id, models.BATCH.batch_number, models.BATCH.stock_id,
                                     models.BATCH.end_date, models.BATCH.start_date, models.BATCH.uom, models.BATCH.bom_id, models.BATCH.plant_id, models.StockMaster.item_code, models.StockMaster.item_name, models.BOM.bom_name, models.Plants.plant_name).select_from(models.BATCH).outerjoin(models.BOM).outerjoin(models.StockMaster).outerjoin(models.Plants).filter(
                    models.BATCH.status == "closed").filter(models.BATCH.end_date >= from_date, models.BATCH.end_date <= to_date)

                get_batch_list = []
                for i in get_batch.all():
                    # get_actual_cost
                    actual_cost = actualCostRawMaterail(i.id, db)
                    i1 = i._asdict()
                    i1["actual_material_cost"] = actual_cost
                    # get_actual_overhead
                    actual_oh_cost = actualOverheadCost(i.id, db)
                    i1["actual_oh_cost"] = actual_oh_cost

                    i1["actual_total_cost"] = round(float(
                        actual_cost) + float(actual_oh_cost), 2)

                    # get_standard rate
                    standard_cost = standardCostRawMaterail(
                        i.bom_id, i.end_date, db)
                    i1["standard_material_cost"] = standard_cost

                    # # get_standard_overhead
                    standard_oh_cost = standardOverheadCost(i.bom_id, db)
                    i1["standard_oh_cost"] = standard_oh_cost
                    i1["standard_total_cost"] = round(float(
                        standard_cost) + float(standard_oh_cost), 2)

                    # materail varaince
                    materail_variance = standard_cost - actual_cost
                    i1["materail_variance"] = materail_variance

                    oh_variance = standard_oh_cost - actual_oh_cost
                    i1["oh_variance"] = oh_variance

                    materail_variance = standard_cost - actual_cost

                    i1["total_variance"] = round(i1["standard_total_cost"] - \
                        i1["actual_total_cost"], 2)

                    get_batch_list.append(i1)

                return {"batch_list": (u._asdict() for u in get_batch.all()), "batch_actual_cost": (get_batch_list)}

    except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")
