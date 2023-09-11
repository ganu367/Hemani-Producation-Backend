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

router = APIRouter(prefix="/company", tags=["Company"])

get_db = database.get_db


@router.post("/create-company")
def createCompany(company_logo: Union[UploadFile, None] = None, company_fields: schemas.ComapnyCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        if db.query(models.Company).count() == 0:
            current_company_id = 1
        else:
            last_id = db.query(func.max(models.Company.id)).first()
            current_company_id = last_id[0] + 1

        path = os.getcwd() + "\\company\\" + str(current_company_id)

        if not os.path.exists(path):
            os.makedirs(path)
        try:

            if company_logo is not None:
                new_company_logo = str(
                    current_company_id) + "_"+"clfile"+"_" + company_logo.filename
                contents = company_logo.file.read()

                with open(os.path.join(path, new_company_logo), 'wb') as f:
                    f.write(contents)

                company_logo_file_path = f"{os.getcwd()}\\company\\{str(current_company_id)}\\{new_company_logo}"
            else:
                company_logo_file_path = None

            new_company = models.Company(
                **company_fields.dict(), company_logo=company_logo_file_path)
            db.add(new_company)
            db.commit()
            db.refresh(new_company)

            return {f"Company is created"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")
        finally:
            if company_logo is not None:
                company_logo.file.close()


@router.get("/get-all-company")
def getAllCompany(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        comapny_data = db.query(models.Company).all()
        return comapny_data


@router.get("/get-by-company-ids/{ids}")
def getByCompanyIDs(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        val_company = db.query(models.Company).filter(
            models.Company.id == ids)
        if not val_company.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Company data not found")
        else:
            return val_company.first()


@router.put("/update-company/{ids}")
def updateCompany(ids: int, company_logo: Union[UploadFile, None] = None, company_fields: schemas.ComapnyUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        path = os.getcwd() + "\\company\\" + str(ids)
        if not os.path.exists(path):
            os.makedirs(path)

        try:
            val_company = db.query(models.Company).filter(
                models.Company.id == ids)

            if not val_company.first():
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="Company data not found")
            else:
                if company_logo is not None:
                    if (os.path.exists(str(val_company.first().company_logo))):
                        deleteFile(str(val_company.first().company_logo))

                    new_company_logo = str(
                        ids) + "_"+"clfile"+"_" + company_logo.filename

                    contents = company_logo.file.read()

                    with open(os.path.join(path, new_company_logo), 'wb') as f:
                        f.write(contents)

                    company_logo_file_path = f"{os.getcwd()}\\company\\{str(ids)}\\{new_company_logo}"
                else:
                    company_logo_file_path = None

                company_fields_dict = company_fields.dict()
                company_fields_dict.update(
                    {"company_logo": company_logo_file_path})

                db.query(models.Company).filter(models.Company.id == ids).update(
                    company_fields_dict)

                db.commit()
                return {f"Company is updated"}

        except Exception as error:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(error.orig)}")

        finally:
            if company_logo is not None:
                company_logo.file.close()


@router.delete("/delete-company/{ids}")
def deleteCompany(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        get_company = db.query(models.Company).filter(
            models.Company.id == ids)

        if not get_company.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="Company data not found")
        else:
            try:

                # count the child table
                child_data = db.query(models.Branch).filter(
                    models.Branch.company_id == ids)

                if (child_data.count() == 0):

                    db.query(models.Company).filter(
                        models.Company.id == ids).delete()
                    db.commit()
                    return{f"Company is deleted"}

                else:
                    raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"delete related records {child_data.count()}")
                
            except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")
