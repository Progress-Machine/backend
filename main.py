from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from user.routers import router as user_router
from auth.routers import router as auth_router
from product.routers import router as product_router
from load_env import load_env

load_env()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, err) -> JSONResponse:
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=500,
                        content={"message": f"{base_error_message}. Detail: {str(err)}"})


app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["user"])
app.include_router(product_router, tags=["product"])
