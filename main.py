from fastapi import FastAPI
from auth import router as auth_router
from ads import router as ads_router
from comments import router as comments_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/auth/users", tags=["Auth"])
app.include_router(ads_router, prefix="/shanyraks", tags=["Ads"])
app.include_router(comments_router, prefix="/shanyraks", tags=["Comments"])
