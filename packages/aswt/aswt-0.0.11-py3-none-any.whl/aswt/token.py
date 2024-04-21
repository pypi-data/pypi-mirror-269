import json, struct, os
import base64
import binascii
import time
import logging
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC

logger = logging.getLogger(__name__)

# Default age of a signed token
DEFAULT_AGE=3600  # 1 hour

# give 60 seconds of grace on expiration/not-before times
DEFAULT_GRACE=60

GLOBAL_CONFIG = None

class HMACKey(object):
    digestmod = SHA256
    header = b"HS"
    def __init__(self, key, keyid, default_age=None):
        if isinstance(key,str): key = key.encode('utf-8')
        self.key = key
        self.id = keyid
        self.default_age = default_age

    def verify(self, mac, content):
        if len(mac) != (self.digestmod.digest_size*2):
            raise ValueError("digest not right length")

        h = HMAC.new(self.key, digestmod=self.digestmod)
        h.update(content)

        try:
            h.hexverify(mac) # this throws an error if the signature is wrong
        except:
            logger.exception("verify error on keyid %s mac %s",self.id,mac)
            raise

    def sign(self, content):
        h = HMAC.new(self.key, digestmod=self.digestmod)
        h.update(content)
        return h.hexdigest()

        
class Token(object):
    MAX_STRING = 1024
    def __init__(self, tokenstring=None, key=None, age=None, notnew=False, grace=DEFAULT_GRACE):
        global GLOBAL_CONFIG
        self._dict = {}
        self.dirty = False
        self.digest = None

        if isinstance(key,HMACKey):
            self.key = key
        elif key is not None:
            self.key = GLOBAL_CONFIG['keys'][key]
        elif GLOBAL_CONFIG['default_key'] is not None:
            self.key = GLOBAL_CONFIG['default_key']
        else:
            self.key = None

        if tokenstring is not None:
            if len(tokenstring)>self.MAX_STRING:
                raise ValueError("token too long!")
            self._load(tokenstring,key,grace=grace)
        elif not notnew:
            # initialize a new token
            now = int(time.time())
            if age is None:
                if self.key is not None and self.key.default_age is not None:
                    age = self.key.default_age
                else:
                    age = DEFAULT_AGE
            if age is not None and age!=0: # age of 0 means unlimited
                self['exp'] = now+age
            self['nbf'] = now
        else:
            raise ValueError("token not passed! can't be None")

    @classmethod
    def load(cls, tokenstring, key=None, grace=DEFAULT_GRACE):
        """
        Load an existing token and validate (fail if the token is not valid)
        """
        return cls(tokenstring,key=key,notnew=True,grace=grace)

    def _load(self, tokenstring, key=None, grace=DEFAULT_GRACE):
        global GLOBAL_CONFIG
        if isinstance(tokenstring,str): tokenstring = tokenstring.encode('utf-8')
        header, keyid, digest, jsoncontent = tokenstring.split(b'.')
        while jsoncontent[-1] in b"\n \r\t":
            jsoncontent = jsoncontent[:-1]
        
        if header != b"HS":
            raise ValueError("incorrect header")
        
        keyid = keyid.decode('utf-8')

        if key is not None:
            # a key was specified! make sure it matches what key is in the token
            if isinstance(key,HMACKey):
                if key.id!=keyid:
                    raise KeyError("key mismatch", key.id, keyid)
                self.key = key
            elif isinstance(key,str):
                if key != keyid:
                    raise KeyError("key mismatch", key, keyid)
                if key not in GLOBAL_CONFIG['keys']:
                    raise KeyError("can't find keyid in keys!",keyid)
                self.key = GLOBAL_CONFIG['keys'][keyid]

        else: # key is None
            key = self.key
            if key.id != keyid: # no key was specified so we can lookup the key if it's in our config
                if keyid not in GLOBAL_CONFIG['keys']:
                    raise KeyError("can't find keyid in keys!",keyid)
                self.key = GLOBAL_CONFIG['keys'][keyid]

        assert self.key is not None
        self.key.verify(digest, jsoncontent)
        self.digest = digest.decode('utf-8')

        self._dict = json.loads(base64.b64decode(jsoncontent).decode('utf-8'))

        # now enforce any time limits in the token        
        if 'exp' not in self or 'nbf' not in self:
            logger.warning("token missing exp and nbf claims - digest=%s",self.digest)
            raise ValueError("must have an expiration and not before set in token")
        now = time.time()
        # give (by default) 60 seconds grace
        if (self['nbf']-grace) > now:
            logger.warning("token not yet valid digest=%s nbf=%d",self.digest,self['nbf'])
            raise ValueError("token not yet valid!")
        if (self['exp']+grace) < now:
            logger.warning("token expired digest=%s exp=%d",self.digest,self['exp'])
            raise ValueError("token expired!")

    def dump(self, key=None):
        """
        Sign Token and return as bytes
        """
        if key is None:
            key = self.key
        if key is None:
            raise ValueError("no key specified and no default key setup! Set ASWT_CONFIG environment variable")

        # encode our token
        # use of separators generates more compact JSON
        data = json.dumps(self._dict,separators=(',',':')).encode('utf-8')
        data = base64.b64encode(data)

        # now sign it
        hashfordata = key.sign(data)
        self.digest = hashfordata

        if '.' in key.id:
            raise ValueError("Key id can't contain a period!",key.id)

        #logger.debug("dumps - hashfordata = %s",h.hexdigest())
        data = b'HS.'+(key.id.encode('utf-8'))+b'.'+hashfordata.encode('utf-8')+b'.'+data

        return data

    def dumps(self,key=None):
        """
        Sign Token and return as str
        """
        return self.dump(key).decode('utf-8')

    def __setitem__(self, name, value):
        # FIXME: we can't go dirty on changes in child objects because only
        # __getitem__ is called in those cases... :(
        if name in self._dict:
            oldvalue = self._dict[name]
            self._dict[name] = value
            # only mark dirty if we changed the value
            if value != oldvalue: self.dirty = True
        else:
            # it's a new value, we are dirty
            self.dirty = True
            self._dict[name] = value

    def __delitem__(self, name):
        del self._dict[name]
        self.dirty = True

    def __getitem__(self, name):
        return self._dict[name]

    def __contains__(self,name):
        return name in self._dict

    def items(self):
        return self._dict.items()

    def get(self, name, default=None):
        if name in self._dict: return self._dict[name]
        else: return default

def new_key(age=None):
    r = Random.new()
    key = r.read(SHA256.digest_size)
    keyid = binascii.hexlify(r.read(4)).decode('utf-8')
    keydata = {'key':binascii.hexlify(key).decode('utf-8'),'keyid':keyid}
    if age is not None:
        keydata['age'] = age
    return keydata

# FINISHME
# 1. pull config/key location from environment
# 2. if gsutil URL, then go to google cloud storage for the file
# 3. Load keys into an array (or dict by keyid?) and automatically use with the wrappers above
def download_gcs_to_string(bucket,filename):
    global GOOGLE_CLOUD_STORAGE_CLIENT
    import google.cloud.storage
    GOOGLE_CLOUD_STORAGE_CLIENT = google.cloud.storage.Client()
    return GOOGLE_CLOUD_STORAGE_CLIENT.bucket(bucket).blob(filename).download_as_string()

def load_config(config=None):
    global GLOBAL_CONFIG
    GLOBAL_CONFIG = {'keys':{},'default_key':None}
    if config is not None:
        config = json.loads(config)

        keys = [HMACKey(key=binascii.unhexlify(keyconfig['key']), keyid=keyconfig['keyid'], default_age=(keyconfig['age'] if 'age' in keyconfig else None)) for keyconfig in config['keys']]
        for key in keys:
            GLOBAL_CONFIG['keys'][key.id] = key
        
        # choose a default key
        if 'default_key' in config and config['default_key'] in GLOBAL_CONFIG['keys']:
            GLOBAL_CONFIG['default_key'] = GLOBAL_CONFIG['keys'][config['default_key']]
        elif len(keys):
            GLOBAL_CONFIG['default_key'] = keys[0]

def get_config(configpath):
    if configpath is not None:
        if configpath.startswith("{"):
            # it's JSON, try to consume as config
            return configpath
        if configpath.startswith('gs://'):
            bucket, blob = configpath[5:].split('/',1)
            config = download_gcs_to_string(bucket,blob)
        else:
            with open(configpath,"r") as fo:
                config = fo.read()
        return config
    else:
        return None

def is_key_set():
    global GLOBAL_CONFIG
    return GLOBAL_CONFIG['default_key'] is not None

def reload_config():
    load_config(get_config(os.environ['ASWT_CONFIG'] if 'ASWT_CONFIG' in os.environ else None))
reload_config()
