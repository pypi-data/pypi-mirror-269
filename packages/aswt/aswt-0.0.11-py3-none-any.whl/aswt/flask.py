import json, struct, os
import logging
from .token import Token, is_key_set
from .require import require_aswt

logger = logging.getLogger(__name__)

import flask

def FlaskCookie(name):
    def get_cookie():
        return flask.request.cookies.get(name)
    return get_cookie

def FlaskForm(name):
    def get_value():
        return flask.request.form.get(name)
    return get_value

def FlaskAuthorization():
    def get_token():
        authheader = flask.request.headers.get('Authorization')
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

def FlaskUnauthorized():
    return "Unauthorized", 403
def FlaskMissingToken():
    return "Missing Token",401
def FlaskMissingClaim(claim):
    return "Missing Claim %s"%(claim), 403

def require(token_sources, required_claims=None, authz=None, pass_token=False, token_required=True):
    return require_aswt(token_sources, required_claims=required_claims, authz=authz, pass_token=pass_token, token_required=token_required,
            missing_claim=FlaskMissingClaim, missing_token=FlaskMissingToken, unauthorized=FlaskUnauthorized)

