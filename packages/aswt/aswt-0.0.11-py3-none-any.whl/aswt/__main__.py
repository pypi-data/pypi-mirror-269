import json, os.path
import logging
import argparse, sys
from .token import Token, new_key, load_config, GLOBAL_CONFIG

logger = logging.getLogger(__name__)

print(repr(sys.argv))
parser = argparse.ArgumentParser()
parser.add_argument('--new-key',action="store_true")
parser.add_argument('--new-token',action="store_true")
parser.add_argument("--keyid",default=None)
parser.add_argument('--verify-token',action="store_true")
parser.add_argument('--claim',action="append")
parser.add_argument('--age',type=int,default=None)
parser.add_argument('config_file',nargs='?')
args = parser.parse_args()

if args.config_file and os.path.exists(args.config_file):
    with open(args.config_file,"r") as fo:
        rawconfig = fo.read()
    config = json.loads(rawconfig)
else:
    config = {'keys':[]}
    rawconfig = None
dirty = False
if args.new_key:
    keydata = new_key(args.age)
    # insert the new key at the beginning (so it becomes the default signing key)
    config['keys'].insert(0,keydata)
    dirty = True
elif args.new_token:
    if rawconfig is None:
        raise ValueError("Missing config file with keys!")
    load_config(rawconfig)
    if GLOBAL_CONFIG['default_key'] is None:
        raise ValueError("No signing key found!")
    t = Token(key=args.keyid,age=args.age)
    for claim in args.claim:
        key,value = claim.split('=',1)
        key = key.strip()
        value = value.strip()
        if value[0:1] in ['[','{']:
            sys.stderr.write("converting %s to json\n"%(value))
            value = json.loads(value)
        t[key]=value
    print(t.dumps())
elif args.verify_token:
    if rawconfig is None:
        raise ValueError("Missing config file with keys!")
    load_config(rawconfig)
    TOKEN = sys.stdin.read()
    t = Token.load(TOKEN)
    print("valid!")

if dirty:
    print(json.dumps(config))
    with open(args.config_file,"w") as fobj:
        fobj.write(json.dumps(config))
        fobj.write("\n")
