from dotenv import load_dotenv
from os import getenv
import requests
import subprocess
import sys
import time

process = subprocess.Popen([
    sys.executable,
    r'C:\Users\lasse\Desktop\Homelab bot\bot.py'
])

load_dotenv()

test_messages = [
    '!pm',
    '!proxmox',
    '!pm version',
    '!pm nodes',
    '!pm help',
    '!pm invalid command',
    '!uptime',
    '!help'
]

WEBHOOK = getenv("TESTING_WEBHOOK") or ""

def send_webhook(content):
    response = requests.post(
        WEBHOOK,
        json={"content": content}
    )

    response.raise_for_status()

time.sleep(3)

send_webhook("BEGIN TESTING")
for message in test_messages:
    send_webhook(message)
    time.sleep(0.3)
    
time.sleep(0.1)

send_webhook("END TESTING")

process.terminate()
process.wait()