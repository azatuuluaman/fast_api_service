from fastapi import FastAPI
import uvicorn

from user.api.users import router as user_router
from advert.api.adverts import router as advert_router

app = FastAPI(openapi_url="/api/v1//openapi.json", docs_url="/api/v1/docs")

app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(advert_router, prefix="/api/v1/adverts", tags=["adverts"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
