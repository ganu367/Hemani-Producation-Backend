from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from internal import authentication
from routers import batch_actual_oh, company, branch, plant, location, user, stockmaster, uom, standard_cost, actual_cost, bom, process, overhead, batch, bom_stock_details, bom_oh_details, batch_actual_consumption, options, utility

models.Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(company.router)
app.include_router(branch.router)
app.include_router(plant.router)
app.include_router(location.router)
app.include_router(user.router)
app.include_router(stockmaster.router)
app.include_router(uom.router)
app.include_router(standard_cost.router)
app.include_router(actual_cost.router)
app.include_router(bom.router)
app.include_router(process.router)
app.include_router(bom_stock_details.router)
app.include_router(overhead.router)
app.include_router(bom_oh_details.router)
app.include_router(batch.router)
app.include_router(batch_actual_consumption.router)
app.include_router(batch_actual_oh.router)
app.include_router(options.router)
app.include_router(utility.router)
