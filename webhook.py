from dotenv import load_dotenv
from os import getenv
import requests
import rich

load_dotenv()

debug = 0
DEBUG_FILE = ".debug_state"

WEBHOOK = getenv("TESTING_WEBHOOK") or ""

async def send_webhook(content):  
    response = requests.post(
        WEBHOOK,
        json={"content": content}
    )

    response.raise_for_status()
    
def _load_debug():
    global debug
    try:
        with open(DEBUG_FILE, "r") as f:
            debug = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        debug = 0

def _save_debug():
    with open(DEBUG_FILE, "w") as f:
        f.write(str(debug))

_load_debug()

def tdebug():
    global debug
    debug = 1 if debug == 0 else 0
    _save_debug()
    
def print(*objects, sep: str = " ", end: str = "\n", file = None, flush = False):
    rich.print(*objects, sep = sep, end = end, file = file, flush = flush)
    _load_debug()
    if debug == 1: t =  send_webhook(sep.join(str(o) for o in objects))