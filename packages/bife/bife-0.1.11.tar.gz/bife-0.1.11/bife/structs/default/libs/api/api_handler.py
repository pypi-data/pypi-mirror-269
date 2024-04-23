import uvicorn
from config import get_config
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.responses import StreamingResponse


class ApiHandler(FastAPI):

    config = get_config()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def add_router(self, router: APIRouter) -> None:
        self.include_router(router)

    def start(self):

        uvicorn.run(
            'main:api_handler',
            host=self.config.API_HOST,
            port=self.config.API_PORT,
            reload=True,
        )
