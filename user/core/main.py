from fastapi import FastAPI
import uvicorn

from user.api.users import router


app = FastAPI(openapi_url="/api/v1/users/openapi.json", docs_url="/api/v1/users/docs")

app.include_router(router, prefix="/api/v1/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
