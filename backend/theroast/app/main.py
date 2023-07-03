from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from theroast.config import server_config

app = FastAPI(
    title=server_config.PROJECT_NAME, openapi_url=f"{server_config.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if server_config.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in server_config.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)