from starlette.applications import Starlette
from starlette.responses import JSONResponse
from httpx import codes

from src.settings import DEBUG
from src.routes import wiki_route
from src.auth import AuthException

async def server_error(request, exc: AuthException):
    return JSONResponse({'result': str(exc)}, status_code=codes.UNAUTHORIZED)


exception_handlers = {
    AuthException: server_error
}

api = Starlette(debug=DEBUG, routes=[
    wiki_route,
], exception_handlers=exception_handlers)