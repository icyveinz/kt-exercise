from fastapi import FastAPI
import routers.api
from lifespan.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(routers.api.router)


@app.get("/")
async def root():
    return {"message": "Service is running"}
