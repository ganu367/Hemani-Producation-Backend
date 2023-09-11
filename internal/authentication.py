from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database
import schemas
import models
import hashing
import tokens
import oauth2
# from routers import alerts
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

get_db = database.get_db

# user_type = "employer"


@router.post("/login-user")
def loginUser(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    if (db.query(models.User).count() == 0):
        if (request.password == "Pass@1234"):

            admin_user = models.User(username=request.username, created_by=request.username,
                                     password=hashing.Hash.bcrypt(request.password), is_admin=True)
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            access_token = tokens.create_access_token(data={"user": {
                "username": request.username, "isAdmin": True}})

            return {"access_token": access_token, "token_type": "bearer"}

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Incorrect Passwords")

    else:
        val_user = db.query(models.User).filter(
            models.User.username == request.username)

        if not val_user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The user does not exists")
        else:

            # verify password between requesting by a user & database password
            if not hashing.Hash.verify(val_user.first().password, request.password):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Incorrect Passwords")
            else:
                if val_user.first().is_admin == False:
                    get_role = db.query(models.UserRights.role,
                                        models.Plants.id.label("plant_id"),
                                        models.Company.id.label("company_id"),
                                        models.Branch.id.label("branch_id")).join(models.Plants, models.Plants.id == models.UserRights.plant_id).join(models.Branch, models.Branch.id == models.Plants.branch_id).join(models.Company, models.Company.id == models.Branch.company_id).filter(
                        models.UserRights.user_id == val_user.first().id)

                    access_token = tokens.create_access_token(data={"user": {
                        "username": request.username, "plantID": get_role.first().plant_id, "branchID": get_role.first().branch_id, "companyID": get_role.first().company_id, "role": get_role.first().role, "isAdmin": val_user.first().is_admin}})
                    return {"access_token": access_token, "token_type": "bearer"}

                else:
                    access_token = tokens.create_access_token(data={"user": {
                        "username": request.username, "isAdmin": val_user.first().is_admin}})
                    return {"access_token": access_token, "token_type": "bearer"}
