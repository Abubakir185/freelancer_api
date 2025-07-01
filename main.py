from fastapi import FastAPI
from database import Base, engine
from routers import freelancers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Freelancer API")

app.include_router(freelancers.router)