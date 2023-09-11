from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database
import schemas
import models
import hashing
import tokens
import oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/user", tags=["UserRights"])

get_db = database.get_db


@router.post("/create-user")
def create_user(request: schemas.UserCreate, user_right_request: schemas.UserRightsCreate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        val_user = db.query(models.User).filter(
            models.User.username == request.username)
        if not val_user.first():
            try:
                request.password = hashing.Hash.bcrypt(request.password)
                c1 = models.User(**request.dict())
                user_right_request.created_by = request.created_by
                user_right_request.created_on = request.created_on
                c1.user_rights = [models.UserRights(
                    **user_right_request.dict())]

                db.add(c1)
                db.commit()
                db.refresh(c1)
                return "User created"

            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(e.orig)}")
        else:
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{request.username} already exists.")


@router.get("/get-all-users")
def GetAllUser(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:
            data = db.query(models.User, models.UserRights).join(
                models.UserRights, models.User.id == models.UserRights.user_id).filter(models.User.is_admin == False,
                                                                                       models.User.is_active == True)

            # list_user = []
            # for i in data.all():
            #     list_user.append(list(i))
            return (u._asdict() for u in data.all())

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.get("/get-user-by-id/{ids}")
def GetUserById(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not (isAdmin_user == True):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        try:

            get_user = db.query(models.User).filter(
                models.User.id == ids).filter(models.User.is_admin == False, models.User.is_active == True)

            if not get_user.first():

                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail="User not found")
            else:

                data = db.query(models.User, models.UserRights).join(
                    models.UserRights, models.User.id == models.UserRights.user_id).filter(models.User.id == ids).filter(models.User.is_admin == False, models.User.is_active == True).first()

                return (list(data))

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail=f"{str(e.orig)}")


@router.put("/update-user/{ids}")
def updateUSer(ids: int, request: schemas.UserUpdate, user_right_request: schemas.UserRightsUpdate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]
    current_username = current_user_login.user["username"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:

        get_user = db.query(models.User).filter(
            models.User.id == ids)

        if not get_user.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="user data not found")
        else:
            try:

                request.password = hashing.Hash.bcrypt(request.password)
                user_right_request.modified_by = request.modified_by
                user_right_request.modified_on = request.modified_on

                db.query(models.User).filter(
                    models.User.id == ids).update({**request.dict()})

                db.query(models.UserRights).filter(models.UserRights.user_id == ids).update(
                    {**user_right_request.dict()})

                db.commit()

                return "Updated are all fields"

            except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")


@router.delete("/delete-company/{ids}")
def deleteUser(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
    current_user_login = current_user
    isAdmin_user = current_user_login.user["isAdmin"]

    if not isAdmin_user == True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not authenticated")
    else:
        get_user = db.query(models.User).filter(
            models.User.id == ids, models.User.is_admin == False).filter(models.User.is_active == True)

        if not get_user.first():
            raise HTTPException(status_code=status.HTTP_302_FOUND,
                                detail="User data not found")
        else:
            try:

                # count the child table
                child_data = db.query(models.UserRights).filter(
                    models.UserRights.user_id == ids)

                if (child_data.count() == 0):
                    db.query(models.User).filter(
                        models.User.id == ids).delete()
                    db.commit()
                    return{f"User is deleted"}
                else:
                    return {f"delete related records {child_data.count()}"}

            except Exception as error:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_302_FOUND,
                                    detail=f"{str(error.orig)}")
