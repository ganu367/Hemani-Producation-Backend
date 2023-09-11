from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, BIGINT, ForeignKey, DateTime, TIMESTAMP, UniqueConstraint, TEXT, FLOAT, Numeric, CheckConstraint
from database import Base
from sqlalchemy.orm import relationship
current_date = datetime.now()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)


class UserRights(Base):
    __tablename__ = "user_rights"
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey(
        "plant.id"))  # refer from Plant id
    user_id = Column(Integer, ForeignKey(
        "user.id"))  # refer from Plant id
    role = Column(String, nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    # Constraints
    __table_args__ = (UniqueConstraint(
        'plant_id', 'user_id', name='unq_1'),)

    user_rights_plant = relationship(
        "Plants", back_populates="user_rights_plant_onwer")

    user = relationship("User", back_populates="user_rights")


User.user_rights = relationship(
    "UserRights", order_by=UserRights.id, back_populates="user")


class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True)
    company_code = Column(String, unique=True)
    gst_number = Column(String)
    pan_number = Column(String)
    smtp_port = Column(Integer)
    smtp_server = Column(String)
    email_address = Column(String)
    email_password = Column(String)
    company_logo = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    # Relationship           #child
    company_onwer = relationship(
        "Branch", back_populates="branch_child")

    stock_company = relationship(
        "StockMaster", back_populates="stock_company_owner")

    company_uom_owner = relationship(
        "UOM", back_populates="uom_company")


class Branch(Base):
    __tablename__ = "branch"
    id = Column(Integer, primary_key=True, index=True)
    branch_name = Column(String)
    branch_code = Column(String)
    company_id = Column(Integer, ForeignKey(
        "company.id"))  # refer from Company id
    address = Column(String)
    gst_number = Column(String)
    pan_number = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    # Constraints
    # __table_args__ = (UniqueConstraint(
    #     'branch_name', 'company_id', name='unq_2'),)

    __table_args__ = (UniqueConstraint(
        'branch_code', 'company_id', name='unq_3'), UniqueConstraint(
        'branch_name', 'company_id', name='unq_2'))

    # Relationship           #child
    branch_child = relationship(
        "Company", back_populates="company_onwer")

    branch_onwer = relationship(
        "Plants", back_populates="plants_child")

    branch_onwer_location = relationship(
        "Location", back_populates="location_child_branch")


class Plants(Base):
    __tablename__ = "plant"
    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String)
    plant_code = Column(String)
    company_id = Column(Integer, ForeignKey(
        "company.id"))  # refer from Company id
    branch_id = Column(Integer, ForeignKey(
        "branch.id"))  # refer from Branch id
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    # Constraints
    # __table_args__ = (UniqueConstraint(
    #     'plant_name', 'branch_id', name='unq_4'),)

    __table_args__ = (UniqueConstraint(
        'plant_code', 'branch_id', name='unq_5'), UniqueConstraint(
        'plant_name', 'branch_id', name='unq_4'))

    # # Relationship           #child
    # Company.Plants = relationship("Plants", order_by = Invoice.id, back_populates = "customer")

    plants_child = relationship(
        "Branch", back_populates="branch_onwer")

    plants_onwer = relationship(
        "Location", back_populates="location_child_plant")

    user_rights_plant_onwer = relationship(
        "UserRights", back_populates="user_rights_plant")


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String)
    location_code = Column(String)
    company_id = Column(Integer, ForeignKey(
        "company.id"))  # refer from Company id
    branch_id = Column(Integer, ForeignKey(
        "branch.id"))  # refer from Branch id
    plant_id = Column(Integer, ForeignKey(
        "plant.id"))  # refer from Plant id
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)
    # is_deleted = Column(Boolean, default=False)

    # Constraints
    # __table_args__ = (UniqueConstraint(
    #     'location_name', 'branch_id', name='unq_6'),)

    __table_args__ = (UniqueConstraint(
        'location_code', 'branch_id', name='unq_7'), UniqueConstraint('location_name', 'branch_id', name='unq_6'))

    # Relationship           #child
    location_child_branch = relationship(
        "Branch", back_populates="branch_onwer_location")

    # Relationship           #child
    location_child_plant = relationship(
        "Plants", back_populates="plants_onwer")


class StockMaster(Base):
    __tablename__ = "stock_master"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    item_code = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    item_desc = Column(String, nullable=False)
    uom = Column(String, nullable=False)

    item_category = Column(String, default="Raw Material")
    hsn_sa_code = Column(Integer)
    item_image = Column(String)
    item_type = Column(String, default="Goods")
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    # __table_args__ = (UniqueConstraint(
    # 'company_id', 'item_code', name='unq_8'),)

    __table_args__ = (UniqueConstraint(
        'company_id', 'item_name', name='unq_9'), UniqueConstraint('company_id', 'item_code', name='unq_8'))

    stock_company_owner = relationship(
        "Company", back_populates="stock_company")

    stock_standard_cost_owner = relationship(
        "StandardCost", back_populates="stock_standard_cost")

    stock_actual_cost_owner = relationship(
        "ActualCost", back_populates="stock_actual_cost")

    stock_bom_owner = relationship(
        "BOM", back_populates="stock_bom")


class UOM(Base):
    __tablename__ = "uom"
    id = Column(Integer, primary_key=True, index=True)
    uom_name = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"))
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'uom_name', 'company_id', name='unq_10'),)

    uom_company = relationship(
        "Company", back_populates="company_uom_owner")


class StandardCost(Base):
    __tablename__ = "standard_cost"
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock_master.id"))
    from_date = Column(DateTime)
    uom = Column(String)
    rate = Column(Numeric(precision=10, scale=2))
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'stock_id', 'from_date', name='unq_11'),)

    stock_standard_cost = relationship(
        "StockMaster", back_populates="stock_standard_cost_owner")


class ActualCost(Base):
    __tablename__ = "actual_cost"
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock_master.id"))
    from_date = Column(DateTime)
    uom = Column(String)
    rate = Column(Numeric(precision=10, scale=2))
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'stock_id', 'from_date', name='unq_12'),)

    stock_actual_cost = relationship(
        "StockMaster", back_populates="stock_actual_cost_owner")


class BOM(Base):
    __tablename__ = "bom"
    id = Column(Integer, primary_key=True, index=True)
    bom_name = Column(String)
    stock_id = Column(Integer, ForeignKey("stock_master.id"))
    bom_quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    uom = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'bom_name', 'stock_id', name='unq_13'),)

    stock_bom = relationship(
        "StockMaster", back_populates="stock_bom_owner")

    # process_bom_onwer = relationship(
    #     "PROCESS", back_populates="stock_process")


class PROCESS(Base):
    __tablename__ = "process"
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("bom.id"))
    process_name = Column(String)
    process_sequence = Column(Integer, default=1)
    # uom = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'bom_id', 'process_name', name='unq_14'),)

    # stock_process = relationship(
    #     "BOM", back_populates="process_bom_onwer")

    bom = relationship(
        "BOM", back_populates="process")


BOM.process = relationship(
    "PROCESS", order_by=PROCESS.id, back_populates="bom")


class BOM_STOCK_DETAILS(Base):
    __tablename__ = "bom_stock_details"
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("bom.id"))
    stock_id = Column(Integer, ForeignKey("stock_master.id"))
    process_id = Column(Integer, ForeignKey("process.id"))
    bom_quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    in_out = Column(String, default="in")
    uom = Column(String)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'bom_id', "process_id", 'stock_id', name='unq_15'),)

    stock_bom = relationship(
        "BOM")

    stock_bom_dt = relationship(
        "StockMaster")

    stock_process_details = relationship(
        "PROCESS")


class OH(Base):
    __tablename__ = "overhead"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    overhead_name = Column(String, nullable=False)
    overhead_uom = Column(String)
    overhead_rate = Column(Numeric(precision=10, scale=2))
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'overhead_name', 'company_id', name='unq_10'),)

    uom_company = relationship(
        "Company")


class BOM_OH_DETAILS(Base):
    __tablename__ = "bom_oh_details"
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("bom.id"))
    process_id = Column(Integer, ForeignKey("process.id"))
    overhead = Column(String)
    oh_uom = Column(String)
    oh_quantity = Column(Numeric(precision=10, scale=2))
    oh_cost = Column(Numeric(precision=10, scale=2))
    oh_rate = Column(Numeric(precision=10, scale=2), nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'bom_id', "process_id", 'overhead', name='unq_16'),)

    oh_bom = relationship(
        "BOM")

    oh_process_details = relationship(
        "PROCESS")


class BATCH(Base):
    __tablename__ = "batch"
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("bom.id"))
    stock_id = Column(Integer, ForeignKey("stock_master.id"))
    plant_id = Column(Integer, ForeignKey(
        "plant.id"))  # refer from Plant id
    batch_number = Column(String)
    batch_number_id = Column(Integer)
    status = Column(String, default="open")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    uom = Column(String)
    batch_quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'bom_id', "process_id", 'overhead', name='unq_16'),)

    __table_args__ = (
        CheckConstraint('end_date > start_date'),
    )

    batch_bom = relationship(
        "BOM")

    batch_stock = relationship(
        "StockMaster")

    batch_plants = relationship("Plants")


class BATCH_ACTUAL_CONSUMPTION(Base):
    __tablename__ = "batch_actual_consumption"
    id = Column(Integer, primary_key=True, index=True)
    entry_number = Column(String)
    entry_sr_number = Column(Integer, default=1)
    batch_id = Column(Integer, ForeignKey("batch.id"))
    stock_id = Column(Integer, ForeignKey("stock_master.id"))
    plant_id = Column(Integer, ForeignKey(
        "plant.id"))  # refer from Plant id
    process_id = Column(Integer, ForeignKey("process.id"))
    location_id = Column(Integer, ForeignKey("location.id"))
    batch_actual_number_id = Column(Integer)
    entry_date = Column(DateTime)
    uom = Column(String)
    quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    in_out = Column(String, default="in")
    actual_rate = Column(Numeric(precision=10, scale=2))
    standard_rate = Column(Numeric(precision=10, scale=2))
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    __table_args__ = (UniqueConstraint(
        'entry_number', "entry_sr_number", 'stock_id', name='unq_17'),)

    batch_acutal = relationship(
        "BATCH")

    batch_actual_stock = relationship(
        "StockMaster")

    batch__actual_plants = relationship("Plants")

    batch__actual_process = relationship(
        "PROCESS")

    batch__actual_location = relationship(
        "Location")


class BATCH_ACTUAL_OH(Base):
    __tablename__ = "batch_actual_oh"
    id = Column(Integer, primary_key=True, index=True)
    entry_number = Column(String)
    entry_sr_number = Column(Integer, default=1)
    batch_id = Column(Integer, ForeignKey("batch.id"))
    # stock_id = Column(Integer, ForeignKey("stock_master.id"))
    plant_id = Column(Integer, ForeignKey(
        "plant.id"))  # refer from Plant id
    process_id = Column(Integer, ForeignKey("process.id"))
    batch_actual_number_id = Column(Integer)
    entry_date = Column(DateTime)
    overhead = Column(String)
    oh_quantity = Column(Numeric(precision=10, scale=2))
    oh_uom = Column(String)
    oh_cost = Column(Numeric(precision=10, scale=2))
    oh_rate = Column(Numeric(precision=10, scale=2), nullable=False)
    created_by = Column(String)
    created_on = Column(DateTime)
    modified_by = Column(String)
    modified_on = Column(DateTime)

    # __table_args__ = (UniqueConstraint(
    #     'entry_number', "plant_id", name='unq_17'),)

    batch_acutal = relationship(
        "BATCH")

    # batch_actual_stock = relationship(
    #     "StockMaster")

    batch__actual_plants = relationship("Plants")

    batch__actual_process = relationship(
        "PROCESS")
