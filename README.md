# gh-webhook-runner

Simple utility based on `https://github.com/bloomberg/python-github-webhook` to run scripts on WebHook  response

## Example usage

```yaml
---
services:
  webhook-runner:
    image: helife/gh-webhook-runner:latest
    environment:
      GH_WEBHOOK_SECRET_FILE: /data/webhook-secret.txt
      GH_WEBHOOK_SCRIPT_INTERPRETOR: 'python3'
      GH_WEBHOOK_SCRIPT_FILE: /data/script.py
      GH_WEBHOOK_ENDPOINT: /gh-webhook
    volumes:
      - ./data:/data:ro
```

Note that in this case /data is read only (for security measures we do not want that the scripts runned everytime may be modified by some parties somehow)
If you want to modify data of another folder I recommended to not put both in the same one

## Run Mode

The `DIR_LOCATION` will be determined by `dirname "$(realpath "$GH_WEBHOOK_SCRIPT_FILE")"`
The `FILENAME` will be determined by `basename "$(realpath "$GH_WEBHOOK_SCRIPT_FILE")"`

## Run native compiled binaries

Set the `SCRIPT_INTERPRETOR` as `native` and the script will be run as a normal executable.
Just make sure to compile the binary with the coresponding arch of your docker engine
