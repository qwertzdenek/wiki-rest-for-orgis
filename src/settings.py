
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
WIKI_CLIENT_ID = config('WIKI_CLIENT_ID', cast=Secret, default=None)
WIKI_CLIENT_SECRET = config('WIKI_CLIENT_SECRET', cast=Secret, default=None)
WIKI_ACCESS_TOKEN = config('WIKI_ACCESS_TOKEN', cast=Secret, default=None)