import time
import random
import string
import logging

import uvicorn
from fastapi import FastAPI, Request

from user.api.users import router as user_router
from advert.api.adverts import router as advert_router

logging.basicConfig(
    filename="fast.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

app = FastAPI(openapi_url="/api/v1//openapi.json", docs_url="/api/v1/docs")

app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(advert_router, prefix="/api/v1/adverts", tags=["adverts"])


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.warning(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.warning(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
