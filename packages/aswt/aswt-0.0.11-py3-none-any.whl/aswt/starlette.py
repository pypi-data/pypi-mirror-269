import json, struct, os
import logging
from .token import Token, is_key_set
from .require import require_aswt_async

logger = logging.getLogger(__name__)

from functools import wraps

import starlette.responses

def StarletteCookie(name):
    async def get_cookie(request):
        return request.cookies.get(name)
    return get_cookie

def StartletteForm(name):
    async def get_value():
        f = await request.form()
        return f.get(name)
    return get_value

def StarletteAuthorization():
    async def get_token(request):
        authheader = request.headers.get('Authorization')
        if authheader is not None:
            tokentype,tokenraw = authheader.split(' ')
            if tokentype == "Bearer":
                return tokenraw
            elif tokentype == "Basic":
                username, _, token = base64.b64decode(tokenraw).decode('ascii').partition(':')
                # ignore the username
                return token
        return None
    return get_token

def StarletteUnauthorized():
    return starlette.responses.Response("Unauthorized",status_code=403)
def StarletteMissingToken():
    return starlette.responses.Response("Missing Token",status_code=401, headers={"WWW-Authenticate":"Basic"})
def StarletteMissingClaim(claim):
    return starlette.responses.Response("Missing Claim %s"%(claim),status_code=403)

def require(token_sources, required_claims=None, authz=None, pass_token=False):
    return require_aswt_async(token_sources, required_claims=required_claims, authz=authz, pass_token=pass_token, missing_claim=StarletteMissingClaim, missing_token=StarletteMissingToken, unauthorized=StarletteUnauthorized)

