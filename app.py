#!/usr/bin/env python3
from github_webhook import Webhook
from flask import Flask
from os import getenv
from subprocess import run as subprocess_run
from pathlib import Path

CONFIG = {
    'GH_WEBHOOK_SECRET_FILE': getenv('GH_WEBHOOK_SECRET_FILE'),
    'GH_WEBHOOK_SCRIPT_INTERPRETOR': getenv('GH_WEBOOK_SCRIPT_INTERPRETOR', "native"),
    'GH_WEBHOOK_SCRIPT_FILE': getenv('GH_WEBOOK_SCRIPT_COMMAND'),
    'GH_WEBHOOK_ENDPOINT': getenv('GH_WEBHOOK_ENDPOINT', '/gh-webhook'),
}

def load_config():
    for key, value in CONFIG.items():
        if not value:
            raise Exception(f'{key} is not set or empty')

    if Path.exists(Path(CONFIG['GH_WEBHOOK_SECRET_FILE'])):
        with open(CONFIG['GH_WEBHOOK_SECRET_FILE'], 'r') as f:
            CONFIG['GH_WEBHOOK_SECRET'] = f.read().strip()
        if not CONFIG['GH_WEBHOOK_SECRET']:
            raise Exception(f'{CONFIG["GH_WEBHOOK_SECRET_FILE"]} is empty')
    else:
        raise Exception(f'{CONFIG["GH_WEBHOOK_SECRET_FILE"]} does not exist')

app = Flask(__name__)
webhook = Webhook(app, endpoint=CONFIG['GH_WEBHOOK_ENDPOINT'], secret=CONFIG['GH_WEBHOOK_SECRET'])
print(f'Starting webhook server on {CONFIG["GH_WEBHOOK_ENDPOINT"]}')

@app.route("/", methods=['POST'])
def index():
    return 'ON'

@webhook.hook()
def on_push(data):
    if CONFIG['GH_WEBHOOK_SCRIPT_INTERPRETOR'] == "native":
        subprocess_run([CONFIG['GH_WEBHOOK_SCRIPT_COMMAND']], shell=False)
    else:
        subprocess_run(["bash", "command-runner.sh", CONFIG['GH_WEBHOOK_SCRIPT_FILE'], CONFIG['GH_WEBHOOK_SCRIPT_INTERPRETOR']], shell=False)

if __name__ == "__main__":
    for key, value in CONFIG.items():
        if value is None:
            raise Exception(f'{key} is not set')
    app.run(host='0.0.0.0', port=80)
