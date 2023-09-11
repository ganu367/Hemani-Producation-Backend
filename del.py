
# @router.get("/get-actual-batch-oh-by-ids/{ids}")
# def GetActualBatchOH(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to view Process")
#         else:
#             get_batch_oh = db.query(models.BATCH_ACTUAL_OH).filter(
#                 models.BATCH_ACTUAL_OH.id == ids)

#             if get_batch_oh.first():
#                 try:

#                     data = db.query(models.BATCH_ACTUAL_OH, models.BATCH, models.StockMaster, models.PROCESS, models.Plants).join(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_OH.batch_id).join(
#                         models.StockMaster, models.StockMaster.id == models.BATCH.stock_id).join(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_OH.process_id).join(models.Plants, models.Plants.id == models.BATCH_ACTUAL_OH.plant_id).filter(models.BATCH_ACTUAL_OH.id == ids)

#                     return (data.first()._asdict())

#                 except Exception as e:
#                     db.rollback()
#                     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                         detail=f"{str(e.orig)}")
#             else:
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"Batch Actual overhead not found")


# get_batch_actual_oh = db.query(func.sum(models.BATCH_ACTUAL_OH.oh_cost)).filter(odels.BATCH_ACTUAL_OH.batch_id == batch_id)
        # if not get_batch_actual_oh.first():

        #     return 0
        # else:
        #     return get_batch_actual_oh.first()[0]
# data = db.query(models.BOM_OH_DETAILS.id, models.BOM_OH_DETAILS.overhead, models.BOM_OH_DETAILS.oh_bom, models.BOM_OH_DETAILS.oh_quantity, models.BOM_OH_DETAILS.oh_rate, models.BOM_OH_DETAILS.created_by,
#                 models.BOM_OH_DETAILS.created_on, models.BOM_OH_DETAILS.modified_by, models.BOM_OH_DETAILS.modified_on, models.PROCESS.process_name, models.BOM.bom_name).join(
#     models.PROCESS, models.PROCESS.id == models.BOM_OH_DETAILS.process_id
# ).join(models.BOM, models.BOM.id == models.PROCESS.bom_id)


#  get_batch_oh = db.query(models.BATCH.batch_number, models.BATCH.start_date, models.BATCH.end_date, models.BATCH.batch_quantity, models.BATCH.bom_id, models.BOM.bom_name, models.StockMaster.item_name, models.Plants.plant_name).select_from(models.BATCH).outerjoin(models.BOM).outerjoin(models.StockMaster).outerjoin(
#                 models.Plants).filter(models.BATCH.status == "closed", models.BATCH.stock_id == stock_id, models.BATCH.id == batch_id)

#             get_batch_actual_overhead = db.query(models.PROCESS.process_name, models.BATCH_ACTUAL_OH.overhead, models.BATCH_ACTUAL_OH.oh_uom, models.BATCH_ACTUAL_OH.oh_quantity, models.BATCH_ACTUAL_OH.oh_rate).select_from(models.BATCH_ACTUAL_OH).outerjoin(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_OH.batch_id).outerjoin(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_OH.process_id).outerjoin(
#                 models.Plants, models.Plants.id == models.BATCH_ACTUAL_OH.plant_id).filter(models.BATCH_ACTUAL_OH.batch_id == batch_id)

#             print(get_batch_actual_overhead.all())
#             df = pd.DataFrame.from_dict(get_batch_actual_overhead)
#             df['oh_cost'] = df['oh_rate'] * df['oh_quantity']
#             print(df)

# bom stock detail goes here
# get_bom_oh_details = db.query(models.BOM_OH_DETAILS.bom_id, models.BOM_OH_DETAILS.process_id, models.BOM_OH_DETAILS.oh_quantity,models.PROCESS.process_name).select_from(
#     models.BOM_STOCK_DETAILS).outerjoin(models.PROCESS).filter(models.BOM_STOCK_DETAILS.bom_id == get_batch_oh.first().bom_id)

# actual cost report
# get_oh_data_list = []
# for i in get_batch_actual_overhead.all():
#     # get_actual_rate = actualRate(stock_id, i.entry_date, db)
#     get_standard_rate = standardRate(stock_id, i.entry_date, db)
#     i1 = i._asdict()
#     i1["actual_rate"] = get_actual_rate
#     i1["standard_rate"] = get_standard_rate
#     get_oh_data_list.append(i1)

# print(get_oh_data_list)

# print(df)

# df_actual = df.groupby(['process_name', 'item_code', 'item_name']).agg(
#     {'quantity': "sum", 'actual_cost': "sum"}).reset_index()

# @router.get("/get-batch-ack-consumption-by-ids/{ids}")
# def GetBatchAckConsumptionByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to view Process")
#         else:

#             try:
#                 get_sc = db.query(models.BATCH_ACTUAL_CONSUMPTION, models.BATCH, models.PROCESS, models.Plants, models.StockMaster, models.Location
#                 ).join(
#                     models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id
#                 ).join(
#                     models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_CONSUMPTION.process_id
#                 ).join(
#                     models.StockMaster, models.StockMaster.id == models.BATCH_ACTUAL_CONSUMPTION.stock_id
#                 ).join(
#                     models.Plants, models.Plants.id == models.BATCH_ACTUAL_CONSUMPTION.plant_id
#                 ).join(
#                     models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id
#                 ).filter(models.BATCH_ACTUAL_CONSUMPTION.id == ids)

#                 return (get_sc.first()._asdict())
#             except Exception as e:
#                 db.rollback()
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"{str(e.orig)}")

# if db.query(models.Company).count() == 0:
#     current_company_id = 1
# else:
#     last_id = db.query(func.max(models.Company.id)).first()
#     current_company_id = last_id[0] + 1
#     else:
#         raise HTTPException(status_code=status.HTTP_302_FOUND,
#                             detail=f"{company_fields.company_code} must be unique")
# else:
#     print("Hello there elseee elsee")
#     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                         detail=f"{company_fields.company_name} must be unique")
# pass
# except IntegrityError as e:
#     db.rollback()
#     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                         detail=f"{e}")

# print("Hello there elseee")
# if not val_company.filter(models.Company.company_name == company_fields.company_name).first():
#     print("Hello there......")
#     if not val_company.filter(models.Company.company_code == company_fields.company_code).first():
#         print("Hello there")

# val_user = db.query(models.User).filter(
#       models.User.username == request.username)
#   print(val_user.first().is_admin)
#   if not val_user.first():
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                           detail="The user does not exists")
#   else:
#       # if not val_user.is_admin == True:
#       # verify password between requesting by a user & database password
#       if not hashing.Hash.verify(val_user.first().password, request.password):
#           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                               detail="Incorrect Passwords")
#       else:
#           access_token = tokens.create_access_token(data={"user": {
#               "username": request.username, "isAdmin": val_user.first().is_admin}})
#           return {"access_token": access_token, "token_type": "bearer"}

#       # else:
#       #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#       #                         detail="Not Authenetication")


# ...chaneges for test

# @router.post("/add-company-branch")
# def addCompanyBranch(company_logo: Union[UploadFile, None] = None, company_fields: schemas.ComapnyCreate = Depends(), branch_fields: schemas.CompanyBranchCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     current_username = current_user_login.user["username"]

#     if not (isAdmin_user == True):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if db.query(models.Company).count() == 0:
#             current_company_id = 1
#         else:
#             last_id = db.query(func.max(models.Company.id)).first()
#             current_company_id = last_id[0] + 1

#         path = os.getcwd() + "\\company\\" + str(current_company_id)

#         if not os.path.exists(path):
#             os.makedirs(path)
#         try:

#             if company_logo is not None:
#                 new_company_logo = str(
#                     current_company_id) + "_"+"clfile"+"_" + company_logo.filename

#                 contents = company_logo.file.read()

#                 with open(os.path.join(path, new_company_logo), 'wb') as f:
#                     f.write(contents)

#                 company_logo_file_path = f"{os.getcwd()}\\company\\{str(current_company_id)}\\{new_company_logo}"
#             else:
#                 company_logo_file_path = None

#             # c1.invoices = [Invoice(invno = 10, amount = 15000), Invoice(invno = 14, amount = 3850)]
#             # ..change goes here
#             new_company = models.Company(
#                 **company_fields.dict(), company_logo=company_logo_file_path, created_by=current_username)

#             new_branch = [models.Branch(
#                 **branch_fields.dict(), created_by=current_username)]

#             new_company.branch.append(new_branch)

#             db.add(new_company)
#             db.commit()
#             db.refresh(new_company)

#             return new_company
#         except Exception as e:
#             db.rollback()
#             raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                 detail=f"{str(e)}")
#         finally:
#             if company_logo is not None:
#                 company_logo.file.close()
# db.query(models.Branch.id,func.count().label("count")).filter(models.Branch.company_id==ids)
# print(child_data)
# for i in child_data:
#     print(i.id)
#     row_count = db.query(models.Branch).filter(
#         models.Branch.id == i.id).count()
#     print(row_count)
# db.commit()

# from fastapi import APIRouter, Depends, status, HTTPException, Response
# from sqlalchemy.orm import Session
# import database
# import schemas
# import models
# import hashing
# import tokens
# import oauth2
# from fastapi.security import OAuth2PasswordRequestForm

# router = APIRouter(prefix="/auth", tags=["Registration"])

# get_db = database.get_db


# @router.post("/create-user")
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     val_user = db.query(models.User).filter(
#         models.User.username == request.username)
#     if not val_user.first():
#         try:
#             new_user = models.User(username=request.username, created_by=request.username,
#                                 password=hashing.Hash.bcrypt(request.password))
#             db.add(new_user)
#             db.commit()
#             db.refresh(new_user)
#             return new_user
#         except Exception as e:
#             db.rollback()
#             raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                 detail=f"{str(e.orig)}")
#     else:
#         raise HTTPException(status_code=status.HTTP_302_FOUND,
#                             detail=f"{request.username} already exists.")
# # print(str(**request.dict()))
# print("HI1")
# user_rights_list = []
# for i in user_right_rq:
#     print(i)
#     print("HI2")
#     user_rights_list.append(models.UserRights(**i.dict()))

# c1.user_rights = user_rights_list

# list_branches = " "
# for i in child_data.all():
#     name = db.query(models.Branch.branch_name).filter(
#         models.Branch.id == i.id)
#     list_branches += str(name.first())[2:-3] + ","

# return {f"delete related records {child_data.count()}", child_data.all()}
# get_branch.update({"is_deleted": True, "branch_name": "del_"+str(
#     ids)+"_"+get_branch.first().branch_name, "branch_code": "del_"+str(ids)+"_"+get_branch.first().branch_code})
# db.commit()

# return{f"Branch is deleted"}

# list_branches = " "
# for i in child_data.all():
#     name = db.query(models.Branch.branch_name).filter(
#         models.Branch.id == i.id)
#     list_branches += str(name.first())[2:-3] + ","

# return {f"delete related records {child_data.count()}", child_data.all()}

# @router.post("/create-stock")
# def createStock(stock_image: Union[UploadFile, None] = None, stock_fields: schemas.StockMasterCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     current_username = current_user_login.user["username"]

#     if not (isAdmin_user == True):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if db.query(models.StockMaster).count() == 0:
#             current_stock_id = 1
#         else:
#             last_id = db.query(func.max(models.StockMaster.id)).first()
#             current_stock_id = last_id[0] + 1

#         path = os.getcwd() + "\\company\\" + str(stock_fields.company_id) + \
#             "\\stocks\\" + str(current_stock_id)
#         if not os.path.exists(path):
#             os.makedirs(path)
#         try:

#             if stock_image is not None:
#                 new_stock_img = str(
#                     current_stock_id) + "_"+"sifile"+"_" + stock_image.filename

#                 contents = stock_image.file.read()

#                 with open(os.path.join(path, new_stock_img), 'wb') as f:
#                     f.write(contents)

#                 stock_img_file_path = f"{os.getcwd()}\\company\\{str(stock_fields.company_id)}\\stocks\\{str(current_stock_id)}\\{new_stock_img}"
#                 print(stock_img_file_path)
#             else:
#                 stock_img_file_path = None

#             new_stock = models.StockMaster(
#                 **stock_fields.dict(), item_image=stock_img_file_path)
#             db.add(new_stock)
#             db.commit()
#             db.refresh(new_stock)

#             return {"New stock added"}

#         except Exception as e:
#             db.rollback()
#             raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                 detail=f"{str(e.orig)}")
#         finally:
#             if stock_image is not None:
#                 stock_image.file.close()

# @router.put("/update-bom/{ids}")
# def UpdateBOM(ids: int, bom_fields: schemas.BOMUpdate, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
# current_user_login = current_user
# isAdmin_user = current_user_login.user["isAdmin"]
# current_username = current_user_login.user["username"]
# user_role = current_user_login.user["role"]

# if not (isAdmin_user == False):
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail="not authenticated")
# else:
#     if not (user_role == "Production Executive"):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="You don't have permmission to update BoM")
#     else:

#         try:
#             # db.query(models.BOM).filter(
#             #     models.BOM.id == ids).update(bom_fields.dict())
#             # db.commit()

#             bom_fields_dict = bom_fields.dict()
#             # process =  bom_fields_dict
#             del bom_fields_dict["process"]

#             new_bom = db.query(models.BOM).filter(
#                 models.BOM.id == ids).update(bom_fields_dict)

#             bom = db.query(models.BOM).filter(
#                 models.BOM.id == ids)

#             process_list = []

#             for i in bom_fields.process:
#                 process_list.append(models.PROCESS(**i.dict()))

#             new_bom.process = process_list

#             db.add(new_bom)
#             db.commit()
#             db.refresh(new_bom)

#             db.commit()

#             return {"BoM fields are updated!"}

#         except Exception as e:
#             db.rollback()
#             raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                 detail=f"{str(e.orig)}")
#    if (get_standard_cost.count() == 0):
#                 standard_rate = 0
#                 print(get_standard_cost.count())
#             else:
#                 standard_rate = 0
#                 for i in get_standard_cost.all():
#                     if batch_ack_fields.entry_date >= i.from_date:
#                         standard_rate = i.rate
#                         print(standard_rate)
#                     else:
#                         break

# print(standard_rate)

# get_overhead = db.query(models.OH).filter(
#     models.OH.overhead_name == batch_oh_fields.overhead)

# if not get_overhead.first():
#     overhead_uom = None
#     overhead_rate = None
# else:
#     overhead_uom = get_overhead.first().overhead_uom
#     overhead_rate = get_overhead.first().overhead_rate

# actual_rates = []
# for i in get_quanty.all():
#     print(i.stock_id)
#     print(i.entry_date)

#     get_actual_cost = db.query(models.ActualCost).filter(
#         models.ActualCost.stock_id == i.stock_id).order_by(asc(models.ActualCost.from_date))

#     if (get_actual_cost.count() == 0):
#         actual_rate = 0
#         actual_rates = actual_rates.append(actual_rate)
#     else:
#         actual_rate = 0
#         for j in get_actual_cost.all():
#             if i.entry_date >= j.from_date:
#                 actual_rate = j.rate
#             else:
#                 break
#         actual_rates = actual_rates.append(actual_rate)

# get_consum_data= db.query(models.BATCH_ACTUAL_CONSUMPTION.entry_number,models.BATCH_ACTUAL_CONSUMPTION.entry_sr_number,models.BATCH_ACTUAL_CONSUMPTION.stock_id,models.BATCH_ACTUAL_CONSUMPTION.batch_id,models.BATCH_ACTUAL_CONSUMPTION.process_id,models.BATCH_ACTUAL_CONSUMPTION.location_id,models.BATCH_ACTUAL_CONSUMPTION.plant_id,models.BATCH_ACTUAL_CONSUMPTION.entry_date, models.BATCH_ACTUAL_CONSUMPTION.uom, models.BATCH_ACTUAL_CONSUMPTION.quantity,models.BATCH_ACTUAL_CONSUMPTION.in_out,models.StockMaster.item_name,
#                       models.StockMaster.item_code).outerjoin(models.StockMaster).filter(models.BATCH_ACTUAL_CONSUMPTION.in_out == "in", models.BATCH_ACTUAL_CONSUMPTION.batch_id == batch_id)
# df_actual = df.groupby(['process_name', 'item_code', 'item_name'])[
#     ['quantity', 'actual_cost']].sum()


# @router.get("/all-generate-report/{stock_id}/{batch_id}")
# def GenerateReports(batch_id: int, stock_id: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to view Process")
#         else:

#             # try:
#             # if db.query(models.BATCH).filter(models.BATCH.status == "closed", models.BATCH.stock_id == stock_id, models.BATCH.id == batch_id).first():

#             # batch details goes here
#             get_batch = db.query(models.BATCH.batch_number, models.BATCH.start_date, models.BATCH.end_date, models.BATCH.batch_quantity, models.BATCH.bom_id, models.BOM.bom_name, models.StockMaster.item_name, models.Plants.plant_name).select_from(models.BATCH).outerjoin(models.BOM).outerjoin(models.StockMaster).outerjoin(
#                 models.Plants).filter(models.BATCH.status == "closed", models.BATCH.stock_id == stock_id, models.BATCH.id == batch_id)
#             # print(get_batch.all())

#             # bom stock detail goes here
#             get_bom_stock_details = db.query(models.BOM_STOCK_DETAILS.stock_id, models.BOM_STOCK_DETAILS.process_id, models.BOM_STOCK_DETAILS.bom_quantity, models.StockMaster.item_name, models.StockMaster.item_code, models.PROCESS.process_name).select_from(
#                 models.BOM_STOCK_DETAILS).outerjoin(models.StockMaster).outerjoin(models.PROCESS).filter(models.BOM_STOCK_DETAILS.bom_id == get_batch.first().bom_id, models.BOM_STOCK_DETAILS.in_out == "in")

#             # else:
#             #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#             #                     detail="Records not found")

#             # quantity
#             # batch actual consumption code goes here
#             get_consum_data = db.query(models.BATCH_ACTUAL_CONSUMPTION.entry_number, models.BATCH_ACTUAL_CONSUMPTION.entry_sr_number, models.BATCH_ACTUAL_CONSUMPTION.stock_id, models.BATCH_ACTUAL_CONSUMPTION.location_id, models.BATCH_ACTUAL_CONSUMPTION.batch_id, models.BATCH_ACTUAL_CONSUMPTION.process_id, models.BATCH_ACTUAL_CONSUMPTION.plant_id,
#                                        models.BATCH_ACTUAL_CONSUMPTION.entry_date, models.BATCH_ACTUAL_CONSUMPTION.uom,
#                                        models.BATCH_ACTUAL_CONSUMPTION.quantity, models.BATCH_ACTUAL_CONSUMPTION.in_out, models.StockMaster.item_name,
#                                        models.StockMaster.item_code, models.Location.location_name, models.BATCH.batch_number, models.PROCESS.process_name, models.Plants.plant_name).select_from(models.BATCH_ACTUAL_CONSUMPTION).outerjoin(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id).outerjoin(models.StockMaster, models.StockMaster.id == models.BATCH_ACTUAL_CONSUMPTION.stock_id).outerjoin(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_CONSUMPTION.process_id).outerjoin(models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id).outerjoin(models.Plants, models.Plants.id == models.BATCH_ACTUAL_CONSUMPTION.plant_id).filter(models.BATCH_ACTUAL_CONSUMPTION.in_out == "in", models.BATCH_ACTUAL_CONSUMPTION.batch_id == batch_id)

#             # actual cost report
#             get_consum_data_list = []
#             for i in get_consum_data.all():
#                 get_actual_rate = actualRate(stock_id, i.entry_date, db)
#                 get_standard_rate = standardRate(stock_id, i.entry_date, db)
#                 i1 = i._asdict()
#                 i1["actual_rate"] = get_actual_rate
#                 i1["standard_rate"] = get_standard_rate
#                 get_consum_data_list.append(i1)

#             df = pd.DataFrame.from_dict(get_consum_data_list)

#             df['actual_cost'] = df['actual_rate'] * df['quantity']
#             # print(df['actual_cost'])

#             df_actual = df.groupby(['process_name', 'item_code', 'item_name']).agg(
#                 {'quantity': "sum", 'actual_cost': "sum"}).reset_index()

#             print(df_actual)

#             # standard cost report
#             # print(get_batch.first().end_date)
#             get_standard_rate_list = []
#             for i in get_bom_stock_details.all():
#                 get_standard_rate = standardRate(
#                     i.stock_id, get_batch.first().end_date, db)
#                 i1 = i._asdict()
#                 i1["standard_rate"] = get_standard_rate
#                 get_standard_rate_list.append(i1)

#             # print(get_standard_rate_list)

#             df = pd.DataFrame.from_dict(get_standard_rate_list)
#             df['stadard_cost'] = df['standard_rate'] * df['bom_quantity']
#             df_standard = df.groupby(['process_name', 'item_code', 'item_name']).agg(
#                 {'bom_quantity': "sum", 'stadard_cost': "sum"}).reset_index()

#             print(df_standard)

#             # print(df_actual.merge(df_standard, on="process_name", how='outer'))
#             final_df = pd.merge(df_actual, df_standard, on=[
#                                 'process_name', 'item_code', 'item_name'], how='outer').fillna(0)

#             final_df['quantity_variance'] = final_df['bom_quantity'] - final_df['quantity']
#             final_df['cost_variance'] = final_df['stadard_cost'] - final_df['actual_cost']

#             # final_df['avg_rate'] = final_df['actual_cost']/final_df['quantity']
#             # final_df['std_rate'] = final_df['stadard_cost']/final_df['bom_quantity']

#             print(final_df)

#             return {"Basic": (u._asdict() for u in get_batch.all()), "Consumpation_data": (x._asdict() for x in get_consum_data.all()), "Process_data": (v._asdict() for v in get_bom_stock_details.all()),"consumption":final_df.to_dict()}

#             # return (get_batch.first()._asdict(), {"stock": "syz"})
#             # except Exception as error:
#             #     db.rollback()
#             #     raise HTTPException(status_code=status.HTTP_302_FOUND,
#             #                         detail=f"{str(error.orig)}")


######################################batch Acutal cons####################
# from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile, Query
# from sqlalchemy.orm import Session
# from sqlalchemy import func, asc
# import database
# import schemas
# import models
# import oauth2
# from typing import List, Optional, Union
# import os
# from routers.utility import deleteFile
# from os import getcwd, remove
# import base64
# from typing import Union
# from fastapi.encoders import jsonable_encoder
# from sqlalchemy.exc import IntegrityError
# from datetime import datetime
# current_date = datetime.now()

# router = APIRouter(prefix="/batch-actual-consumption",
#                    tags=["Batch Actual Consumption"])

# get_db = database.get_db


# @router.post("/create-batch-ack-consumption")
# def CreateBatchAckConsmuption(batch_ack_fields: schemas.BatchActualConsCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to create batch actual consumption")
#         else:
#             try:
#                 get_count = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
#                     models.BATCH_ACTUAL_CONSUMPTION.plant_id == batch_ack_fields.plant_id)

#                 if get_count.count() == 0:
#                     batch_ack_number = 1
#                 else:
#                     last_id = db.query(func.max(models.BATCH_ACTUAL_CONSUMPTION.batch_actual_number_id)).filter(
#                         models.BATCH_ACTUAL_CONSUMPTION.plant_id == batch_ack_fields.plant_id).first()

#                     batch_ack_number = int(last_id[0]) + 1

#                 get_actual_cost = db.query(models.ActualCost).filter(
#                     models.ActualCost.stock_id == batch_ack_fields.stock_id).order_by(asc(models.ActualCost.from_date))

#                 get_standard_cost = db.query(models.StandardCost).filter(
#                     models.StandardCost.stock_id == batch_ack_fields.stock_id).order_by(asc(models.StandardCost.from_date))

#                 if batch_ack_fields.in_out == "in":

#                     if (get_actual_cost.count() == 0):
#                         actual_rate = 0
#                     else:
#                         actual_rate = 0
#                         for i in get_actual_cost.all():
#                             if batch_ack_fields.entry_date >= i.from_date:
#                                 actual_rate = i.rate
#                             else:
#                                 break

#                     if (get_standard_cost.count() == 0):
#                         standard_rate = 0
#                     else:
#                         standard_rate = 0
#                         for i in get_standard_cost.all():
#                             if batch_ack_fields.entry_date >= i.from_date:
#                                 standard_rate = i.rate
#                             else:
#                                 break

#                 else:
#                     actual_rate = None
#                     standard_rate = None

#                 new_batch_ack_consump = models.BATCH_ACTUAL_CONSUMPTION(
#                     **batch_ack_fields.dict(), entry_number=str(batch_ack_fields.plant_id)+"_"+str(batch_ack_number), batch_actual_number_id=batch_ack_number, actual_rate=actual_rate, standard_rate=standard_rate)

#                 db.add(new_batch_ack_consump)
#                 db.commit()
#                 db.refresh(new_batch_ack_consump)

#                 return {"New batch actual consumption created"}

#             except Exception as e:
#                 db.rollback()
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"{str(e.orig)}")


# @router.get("/get-all-batch-ack-consumption")
# def GetAllBatchAckConsumption(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to view all batch Actual Consumtpion")
#         else:
#             try:
#                 data = db.query(models.BATCH_ACTUAL_CONSUMPTION, models.BATCH.batch_number, models.PROCESS.process_name, models.Plants.plant_name, models.StockMaster.item_name, models.Location.location_name
#                                 ).join(
#                     models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id
#                 ).join(
#                     models.PROCESS, models.PROCESS.bom_id == models.BATCH.bom_id
#                 ).join(
#                     models.BOM, models.BOM.id == models.PROCESS.bom_id
#                 ).join(
#                     models.StockMaster, models.StockMaster.id == models.BOM.stock_id
#                 ).join(
#                     models.Plants, models.Plants.id == models.BATCH.plant_id
#                 ).join(
#                     models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id
#                 )

#                 print(data.all())
#                 return (u._asdict() for u in data.all())

#             except Exception as e:
#                 db.rollback()
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"{str(e.orig)}")


# @router.get("/get-batch-ack-consumption-by-ids/{ids}")
# def GetBatchAckConsumptionByIds(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to view Process")
#         else:

#             try:
#                 get_sc = data = db.query(models.BATCH_ACTUAL_CONSUMPTION, models.BATCH, models.PROCESS, models.Plants, models.StockMaster, models.Location
#                                          ).join(
#                     models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_CONSUMPTION.batch_id
#                 ).join(
#                     models.PROCESS, models.PROCESS.bom_id == models.BATCH.bom_id
#                 ).join(
#                     models.BOM, models.BOM.id == models.PROCESS.bom_id
#                 ).join(
#                     models.StockMaster, models.StockMaster.id == models.BOM.stock_id
#                 ).join(
#                     models.Plants, models.Plants.id == models.BATCH.plant_id
#                 ).join(
#                     models.Location, models.Location.id == models.BATCH_ACTUAL_CONSUMPTION.location_id
#                 ).filter(models.BATCH_ACTUAL_CONSUMPTION.id == ids)

#                 return (get_sc.first()._asdict())
#             except Exception as e:
#                 db.rollback()
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"{str(e.orig)}")


# @router.put("/update-batch-ack-consumption/{ids}")
# def UpdateBatchAckConsumption(ids: int, batch_ack_fields: schemas.BatchActualConsUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     current_username = current_user_login.user["username"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to update Batch Actual Consumption")
#         else:
#             get_batch_ack = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
#                 models.BATCH_ACTUAL_CONSUMPTION.id == ids)
#             if get_batch_ack.first():
#                 try:

#                     get_actual_cost = db.query(models.ActualCost).filter(
#                         models.ActualCost.stock_id == get_batch_ack.first().stock_id).order_by(asc(models.ActualCost.from_date))

#                     get_standard_cost = db.query(models.StandardCost).filter(
#                         models.StandardCost.stock_id == get_batch_ack.first().stock_id).order_by(asc(models.StandardCost.from_date))

#                     if batch_ack_fields.in_out == "in":

#                         if (get_actual_cost.count() == 0):
#                             actual_rate = 0
#                         else:
#                             actual_rate = 0
#                             for i in get_actual_cost.all():
#                                 if batch_ack_fields.entry_date >= i.from_date:
#                                     actual_rate = i.rate
#                                 else:
#                                     break

#                         if (get_standard_cost.count() == 0):
#                             standard_rate = 0
#                         else:
#                             standard_rate = 0
#                             for i in get_standard_cost.all():
#                                 if batch_ack_fields.entry_date >= i.from_date:
#                                     standard_rate = i.rate
#                                 else:
#                                     break

#                     else:
#                         actual_rate = None
#                         standard_rate = None

#                     batch_ack_fields_dict = batch_ack_fields.dict()
#                     batch_ack_fields_dict.update(
#                         {"actual_rate": actual_rate, "standard_rate": standard_rate})

#                     db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
#                         models.BATCH_ACTUAL_CONSUMPTION.id == ids).update(batch_ack_fields_dict)
#                     db.commit()
#                     return {"Batch Actual Consumption fields are updated!"}

#                 except Exception as e:
#                     db.rollback()
#                     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                         detail=f"{str(e.orig)}")
#             else:
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"Batch Actual Consumption not found")


# @router.delete("/delete-batch-ack-consumption/{ids}")
# def DeleteBatchAckConsumption(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to delete Batch Actual Consumption ")
#         else:
#             get_data = db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
#                 models.BATCH_ACTUAL_CONSUMPTION.id == ids)

#             if not get_data.first():
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail="Batch Actual Consumption  data not found")
#             else:
#                 try:
#                     db.query(models.BATCH_ACTUAL_CONSUMPTION).filter(
#                         models.BATCH_ACTUAL_CONSUMPTION.id == ids).delete()
#                     db.commit()
#                     return{f"Batch Actual Consumption is deleted"}

#                 except Exception as error:
#                     db.rollback()
#                     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                         detail=f"{str(error.orig)}")

######################################batch Acutal cons end####################
######################################batch Acutal cons oh####################
from fastapi import APIRouter, Depends, status, Body, Form, HTTPException, File, UploadFile, Query
# from sqlalchemy.orm import Session
# from sqlalchemy import func, asc
# import database
# import schemas
# import models
# import oauth2
# from typing import List, Optional, Union
# import os
# from routers.utility import deleteFile
# from os import getcwd, remove
# import base64
# from typing import Union
# from fastapi.encoders import jsonable_encoder
# from sqlalchemy.exc import IntegrityError
# from datetime import datetime
# current_date = datetime.now()

# router = APIRouter(prefix="/batch-actual",
#                    tags=["Batch Actual Overhead"])

# get_db = database.get_db


# @router.post("/create-batch-actual-oh")
# def CreateActualBatchOH(batch_oh_fields: schemas.BatchActualOHCreate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to create batch actual overhead")
#         else:
#             try:
#                 get_count = db.query(models.BATCH_ACTUAL_OH).filter(
#                     models.BATCH_ACTUAL_OH.plant_id == batch_oh_fields.plant_id)

#                 if get_count.count() == 0:
#                     batch_oh_number = 1
#                 else:
#                     last_id = db.query(func.max(models.BATCH_ACTUAL_OH.batch_actual_number_id)).filter(
#                         models.BATCH_ACTUAL_OH.plant_id == batch_oh_fields.plant_id).first()

#                     batch_oh_number = int(last_id[0]) + 1

#                 new_batch_oh = models.BATCH_ACTUAL_OH(
#                     **batch_oh_fields.dict(), entry_number=str(batch_oh_fields.plant_id)+"_"+str(batch_oh_number), batch_actual_number_id=batch_oh_number)

#                 db.add(new_batch_oh)
#                 db.commit()
#                 db.refresh(new_batch_oh)

#                 return {"New batch actual Overhead created"}

#             except Exception as e:
#                 db.rollback()
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"{str(e.orig)}")


# @router.get("/get-all-actual-batch-oh")
# def GetAllActulaBatchOH(db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to view all batch Actual Consumtpion")
#         else:
#             try:
#                 data = db.query(models.BATCH_ACTUAL_OH, models.BATCH.id, models.StockMaster.item_name, models.PROCESS.process_name, models.Plants.plant_name).join(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_OH.batch_id).join(
#                     models.StockMaster, models.StockMaster.id == models.BATCH.stock_id).join(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_OH.process_id).join(models.Plants, models.Plants.id == models.BATCH_ACTUAL_OH.plant_id)
#                 return (u._asdict() for u in data.all())

#             except Exception as e:
#                 db.rollback()
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"{str(e.orig)}")


# @router.get("/get-actual-batch-oh-by-ids/{ids}")
# def GetActualBatchOH(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to view Process")
#         else:
#             get_batch_oh = db.query(models.BATCH_ACTUAL_OH).filter(
#                 models.BATCH_ACTUAL_OH.id == ids)

#             if get_batch_oh.first():
#                 try:

#                     data = db.query(models.BATCH_ACTUAL_OH, models.BATCH, models.StockMaster, models.PROCESS, models.Plants).join(models.BATCH, models.BATCH.id == models.BATCH_ACTUAL_OH.batch_id).join(
#                         models.StockMaster, models.StockMaster.id == models.BATCH.stock_id).join(models.PROCESS, models.PROCESS.id == models.BATCH_ACTUAL_OH.process_id).join(models.Plants, models.Plants.id == models.BATCH_ACTUAL_OH.plant_id).filter(models.BATCH_ACTUAL_OH.id == ids)

#                     return (data.first()._asdict())

#                 except Exception as e:
#                     db.rollback()
#                     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                         detail=f"{str(e.orig)}")
#             else:
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"Batch Actual overhead not found")


# @router.put("/update-batch-actual-oh/{ids}")
# def UpdateActualBatchOH(ids: int, batch_oh_fields: schemas.BatchActualOHUpdate = Depends(), db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     current_username = current_user_login.user["username"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to update Batch Actual")
#         else:
#             get_batch_oh = db.query(models.BATCH_ACTUAL_OH).filter(
#                 models.BATCH_ACTUAL_OH.id == ids)

#             if get_batch_oh.first():
#                 try:
#                     db.query(models.BATCH_ACTUAL_OH).filter(
#                         models.BATCH_ACTUAL_OH.id == ids).update(batch_oh_fields.dict())

#                     db.commit()
#                     return {"Batch Actual Overhead fields are updated!"}

#                 except Exception as e:
#                     db.rollback()
#                     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                         detail=f"{str(e.orig)}")
#             else:
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail=f"Batch Actual not found")


# @router.delete("/delete-actual-batch-oh/{ids}")
# def DeleteActualBatchOH(ids: int, db: Session = Depends(get_db), current_user: schemas.UserBase = Depends(oauth2.get_current_user)):
#     current_user_login = current_user
#     isAdmin_user = current_user_login.user["isAdmin"]
#     user_role = current_user_login.user["role"]

#     if not (isAdmin_user == False):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not authenticated")
#     else:
#         if not (user_role == "Production Executive"):
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                                 detail="You don't have permmission to delete Batch Actual ")
#         else:
#             get_data = db.query(models.BATCH_ACTUAL_OH).filter(
#                 models.BATCH_ACTUAL_OH.id == ids)

#             if not get_data.first():
#                 raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                     detail="Batch Actual overhead data not found")
#             else:
#                 try:
#                     db.query(models.BATCH_ACTUAL_OH).filter(
#                         models.BATCH_ACTUAL_OH.id == ids).delete()
#                     db.commit()
#                     return{f"Batch Actual overhead is deleted"}

#                 except Exception as error:
#                     db.rollback()
#                     raise HTTPException(status_code=status.HTTP_302_FOUND,
#                                         detail=f"{str(error.orig)}")

######################################batch Acutal cons oh end####################
