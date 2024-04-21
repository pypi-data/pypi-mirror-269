"""
It's unfortunate that we have to have multiple critical paths. One for synchronous code
and one for asynchronous code. They are side-by-side here so it's easier to visually
inspect that they're both correct. If one needs a fix or change, make sure to do the same
to the other.

"""
from .token import Token, is_key_set
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def require_aswt(token_sources, required_claims=None, authz=None, pass_token=False, token_required=True,
        missing_claim=None, missing_token=None, unauthorized=None):
    def makewrapper(func):
        @wraps(func)
        def mywrapper(*args,**kwargs):
            if not is_key_set(): raise Exception("default key isn't set!")
            token = None
            logger.debug("checking for valid token")
            try:
                tokenraw = None
                for ts in token_sources:
                    tokenraw = ts()
                    if tokenraw is not None:
                        token = Token.load(tokenraw)
                        break
            except (KeyError,ValueError):
                logger.exception("error parsing token!")
                token = None
            if token is not None:
                logger.info("request_aswt - valid token found with digest=%s", token.digest)
                if required_claims is not None:
                    for claim in required_claims:
                        if claim not in token:
                            logger.warning("request_aswt - missing claim %s on token with digest=%s", claim, token.digest)
                            return missing_claim(claim)
            elif token_required:
                logger.info("request_aswt - no valid token found!")
                return missing_token()

            if authz is not None:
                if not authz(token,**kwargs):
                    logger.warning("request_aswt - failed authz for token with digest=%s", token.digest if token else "(no token)")
                    return unauthorized()
            if pass_token:
                kwargs = kwargs.copy()
                kwargs['token'] = token
            logger.info("request_aswt - access allowed for token with digest=%s", token.digest if token else "(no token)")
            return func(*args,**kwargs)

        return mywrapper
    return makewrapper

def require_aswt_async(token_sources, required_claims=None, authz=None, pass_token=False, missing_claim=None, missing_token=None, unauthorized=None):
    def makewrapper(func):
        @wraps(func)
        async def mywrapper(request,*args,**kwargs):
            if not is_key_set(): raise Exception("default key isn't set!")
            token = None
            logger.debug("checking for valid token")
            try:
                tokenraw = None
                for ts in token_sources:
                    tokenraw = await ts(request)
                    if tokenraw is not None:
                        token = Token.load(tokenraw)
                        break
            except (KeyError,ValueError):
                logger.exception("error parsing token!")
                token = None
            if token is None:
                logger.info("request_aswt_async - no valid token found!")
                return missing_token()
            else:
                logger.info("request_aswt_async - valid token found with digest=%s", token.digest)
                if required_claims is not None:
                    for claim in required_claims:
                        if claim not in token:
                            logger.warning("request_aswt_async - missing claim %s on token with digest=%s", claim, token.digest)
                            return missing_claim(claim)
                if authz is not None:
                    if not authz(token,**kwargs):
                        logger.warning("request_aswt_async - failed authz for token with digest=%s", token.digest)
                        return unauthorized()
                if pass_token:
                    kwargs = kwargs.copy()
                    kwargs['token'] = token
                logger.info("request_aswt_async - access allowed for token with digest=%s", token.digest)
                return await func(request,*args,**kwargs)
        return mywrapper
    return makewrapper

