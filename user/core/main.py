from fastapi import FastAPI

from user.api.users import router


app = FastAPI(openapi_url="/api/v1/users/openapi.json", docs_url="/api/v1/users/docs")


app.include_router(router, prefix="/api/v1/users", tags=["users"])
