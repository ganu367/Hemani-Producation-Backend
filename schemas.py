from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field
from typing import List


class UserBase(BaseModel):
    username: str
    password: str


class UserRightsBase(BaseModel):
    plant_id: int
    role: str

    class config:
        orm_mode = True


class UserCreate(UserBase):
    created_by: str
    created_on: datetime

    class config:

        orm_mode = True


class UserRightsCreate(UserRightsBase):
    created_by: str
    created_on: datetime

    class config:

        orm_mode = True


class UserUpdate(UserBase):
    modified_by: str
    modified_on: datetime

    class config:

        orm_mode = True


class UserRightsUpdate(UserRightsBase):
    modified_by: str
    modified_on: datetime

    class config:

        orm_mode = True


class UserShows(UserBase):
    user_rights: list[UserRightsBase] = []
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime

    class config:

        orm_mode = True


class BatchActualOHBase(BaseModel):
    # entry_sr_number: Optional[int] = None
    # stock_id: int
    # plant_id: int
    process_id: int
    batch_id: int


class BatchActualOHCreate(BatchActualOHBase):
    entry_date: datetime
    overhead: str
    oh_quantity: int
    oh_uom: str
    oh_rate: float
    created_by: str
    created_on: datetime

    class config:
        orm_mode = True


class BatchActualOHCreateList(BaseModel):
    oh_details: List[BatchActualOHCreate] = []

    class config:
        orm_mode = True


class BatchActualOHUpdate(BaseModel):
    entry_date: datetime
    overhead: str
    oh_quantity: float
    oh_uom: str
    oh_rate: float
    modified_by: str
    modified_on: datetime

    class config:
        orm_mode = True


class BatchActualConsBase(BaseModel):
    # entry_sr_number: Optional[int] = None
    batch_id: int
    # plant_id: int
    location_id: int
    stock_id: int
    process_id: int


class BatchActualConsCreate(BatchActualConsBase):
    entry_date: datetime
    uom: str
    quantity: float
    in_out: str
    created_by: str
    created_on: datetime

    class config:
        orm_mode = True


class BatchActualConsCreateList(BaseModel):
    stock_details: List[BatchActualConsCreate] = []

    class config:
        orm_mode = True


class BatchActualConsUpdate(BaseModel):
    entry_date: datetime
    uom: str
    quantity: float
    in_out: str
    location_id: int
    stock_id: int
    modified_by: str
    modified_on: datetime

    class config:
        orm_mode = True


class BatchBase(BaseModel):
    bom_id: int
    stock_id: int
    # plant_id: int


class BatchCreate(BatchBase):
    uom: str
    batch_quantity: float
    # status: Optional[str] = None
    start_date: datetime
    # end_date: Optional[datetime] = None
    created_by: str
    created_on: datetime

    class config:

        orm_mode = True


class BatchUpdate(BaseModel):
    # bom_id: int
    # uom: str
    batch_quantity: float
    # start_date: datetime
    modified_by: str
    modified_on: datetime


class BatchUpdateStatus(BaseModel):
    end_date: datetime
    modified_by: str
    modified_on: datetime


class BoMOHBase(BaseModel):
    bom_id: int
    process_id: int


class BoMOHCreate(BoMOHBase):
    overhead: str
    oh_uom: str
    oh_quantity: float
    oh_rate: float
    created_by: str
    created_on: datetime

    class config:
        orm_mode = True


class BoMOHCreateList(BaseModel):
    oh_details: List[BoMOHCreate] = []

    class config:
        orm_mode = True


class BoMOHUpdate(BaseModel):
    overhead: str
    oh_uom: str
    oh_quantity: float
    oh_rate: float
    modified_by: str
    modified_on: datetime

    class config:
        orm_mode = True


class OHBase(BaseModel):
    overhead_name: str
    overhead_uom: str
    # overhead_rate: float
    # company_id: int


class OHCreate(OHBase):
    created_by: str
    created_on: datetime

    class config:

        orm_mode = True


class OHUpdate(OHBase):
    modified_by: str
    modified_on: datetime

    class config:

        orm_mode = True


class BoMStockDetailsBase(BaseModel):
    stock_id: int
    bom_id: int
    process_id: int


class BoMStockDetailsCreate(BoMStockDetailsBase):
    bom_quantity: float
    in_out: str
    uom: str
    created_by: str
    created_on: datetime

    class config:
        orm_mode = True


class BoMStockDetailsCreateList(BaseModel):
    stock_details: List[BoMStockDetailsCreate] = []

    class config:
        orm_mode = True


class BoMStockDetailsUpdate(BaseModel):
    stock_id: int
    bom_quantity: float
    in_out: str
    uom: str
    modified_by: str
    modified_on: datetime

    class config:
        orm_mode = True
# ............................................


class ProcessBase(BaseModel):
    process_name: str
    process_sequence: Optional[int] = None


class ProcessCreate(ProcessBase):
    # bom_id: int
    created_by: str
    created_on: datetime

    class config:
        orm_mode = True


class ProcessUpdate(ProcessBase):
    # id: int
    modified_by: str
    modified_on: datetime

    class config:
        orm_mode = True


class BOMBase(BaseModel):
    bom_name: str
    bom_quantity: float


class BOMCreate(BOMBase):
    stock_id: int
    uom: str
    created_by: str
    created_on: datetime
    process: List[ProcessCreate] = []

    class config:
        orm_mode = True


class BOMUpdate(BOMBase):
    uom: str
    modified_by: str
    modified_on: datetime
    process: List[ProcessCreate] = []

    class config:
        orm_mode = True

# ..................................................


class ActualCostBase(BaseModel):
    stock_id: int
    from_date: datetime


class ActualCostCreate(ActualCostBase):
    uom: str
    rate: float
    created_by: str
    created_on: datetime

    class config:
        orm_mode = True


class ActualCostUpdate(BaseModel):
    uom: str
    rate: float
    from_date: datetime
    modified_by: str
    modified_on: datetime

    class config:
        orm_mode = True


class StandardCostBase(BaseModel):
    stock_id: int
    from_date: datetime


class StandardCostCreate(StandardCostBase):
    uom: str
    rate: float
    created_by: str
    created_on: datetime

    class config:
        orm_mode = True


class StandardCostUpdate(BaseModel):
    uom: str
    rate: float
    from_date: datetime
    modified_by: str
    modified_on: datetime

    class config:
        orm_mode = True


class StockMasterBase(BaseModel):
    # company_id: int
    item_name: str
    item_code: str
    item_desc: str


class StockMasterCreate(StockMasterBase):
    uom: str
    item_category: str
    hsn_sa_code: Optional[int] = None
    item_type: str
    created_by: str
    created_on: datetime

    class config:

        orm_mode = True


class StockMasterUpdate(StockMasterBase):
    uom: str
    item_category: str
    hsn_sa_code: Optional[int] = None
    item_type: str
    modified_by: str
    modified_on: datetime

    class config:

        orm_mode = True


class StockMasterShows(StockMasterBase):
    uom: str
    item_category: str
    hsn_sa_code: Optional[int] = None
    item_type: str
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime

    class config:

        orm_mode = True


class UOMBase(BaseModel):
    uom_name: str
    # company_id: int


class UOMCreate(UOMBase):
    created_by: str
    created_on: datetime

    class config:

        orm_mode = True


class UOMUpdate(UOMBase):
    modified_by: str
    modified_on: datetime

    class config:

        orm_mode = True


class LocationBase(BaseModel):
    location_name: str
    location_code: str


class LocationCreate(LocationBase):
    branch_id: int
    plant_id: int
    company_id: int
    created_by: str
    created_on: datetime


class LocationUpdate(LocationBase):
    branch_id: int
    plant_id: int
    company_id: int
    modified_by: str
    modified_on: datetime


class LocationShow(LocationCreate):
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime
    is_deleted: bool

    class config:
        orm_mode = True


class PlantBase(BaseModel):
    plant_name: str
    plant_code: str


class PlantCreate(PlantBase):
    branch_id: int
    company_id: int
    created_by: str
    created_on: datetime


class PlantUpdate(PlantBase):
    branch_id: int
    company_id: int
    modified_by: str
    modified_on: datetime


class PlantShow(PlantCreate):
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime
    is_deleted: bool

    class config:
        orm_mode = True


class BranchBase(BaseModel):
    branch_name: str
    branch_code: str


class BranchCreate(BranchBase):
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    address: Optional[str] = None
    company_id: int
    created_by: str
    created_on: datetime


class BranchUpdate(BranchBase):
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    address: Optional[str] = None
    company_id: int
    modified_by: str
    modified_on: datetime


class BranchShow(BranchCreate):
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime
    is_deleted: bool

    class config:
        orm_mode = True


class CompanyBase(BaseModel):
    company_name: str
    company_code: str


class ComapnyCreate(CompanyBase):
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_server: Optional[str] = None
    email_address: Optional[str] = None
    email_password: Optional[str] = None
    created_by: str
    created_on: datetime


class ComapnyUpdate(CompanyBase):
    gst_number: Optional[str] = None
    pan_number: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_server: Optional[str] = None
    email_address: Optional[str] = None
    email_password: Optional[str] = None
    modified_by: str
    modified_on: datetime


class CompanyShow(CompanyBase):
    gst_number: str
    pan_number: str
    smtp_port: int
    smtp_server: str
    email_address: str
    email_password: str
    created_by: str
    created_on: datetime
    modified_by: str
    modified_on: datetime
    is_deleted: bool
    branch: list[BranchShow] = []

    class config:
        orm_mode = True

class GenerateReportsStockWise(BaseModel):
    from_date: datetime
    to_date: datetime

    class config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user: Union[dict, None] = None
