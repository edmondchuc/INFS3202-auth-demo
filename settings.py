from dotenv import load_dotenv

from os import environ

load_dotenv()

AUTH_NAME = 'auth0'
AUTH_CLIENT_ID = environ['AUTH_CLIENT_ID']
AUTH_CLIENT_SECRET = environ['AUTH_CLIENT_SECRET']
AUTH_API_BASE_URL = environ['AUTH_API_BASE_URL']
AUTH_ACCESS_TOKEN_URL = environ['AUTH_ACCESS_TOKEN_URL']
AUTH_AUTHORIZE_URL = environ['AUTH_AUTHORIZE_URL']
AUTH_CALLBACK_URL = environ['AUTH_CALLBACK_URL']
AUTH_LOGOUT_URL = environ['AUTH_LOGOUT_URL']