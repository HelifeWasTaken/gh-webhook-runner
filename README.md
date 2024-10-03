# gh-webhook-runner

**CODE SOON AVAILABLE: Repository is here as placeholder for future**

Simple utility based on `https://github.com/bloomberg/python-github-webhook` to run scripts on WebHook  response

## Example usage using only ENV

```yaml
---
services:
  webhook-runner:
    image: helife/gh-webhook-runner:latest
    environment: 
      # If not specified it will answer at every webhook
      # NEVER SHARE YOUR WEBHOOK SECRET
      GH_WEBHOOK_SECRET: '<REDACTED>' 

      GH_WEBHOOK_SCRIPT_INTERPRETOR: 'bash'
      GH_WEBHOOK_SCRIPT_COMMAND: 'echo "Received webhook call"'
    ports:
      - 80:80 # If you have SSL it would still be better though
```

## Example usage using FILES
```
---
services:
  webhook-runner:
    image: helife/gh-webhook-runner:latest
    environment:
      GH_WEBHOOK_SECRET_FILE: /data/webhook-secret.txt
      GH_WEBHOOK_SCRIPT_INTERPRETOR: 'python3'
      GH_WEBHOOK_SCRIPT_FILE: /data/script.py
    volumes:
      - ./data:/data:ro
```
Note that in this case /data is read only (for security measures we do not want that the scripts runned everytime may be modified by some parties somehow)
If you want to modify data of another folder I recommended to not put both in the same one

## Run Mode

### Command Mode
In `COMMAND` mode the script will be runned from `/`

### File Mode

In `FILE_MODE` a `DIR_LOCATION` and `FILENAME` variable will be created to run based on the script position

The `DIR_LOCATION` will be determined by `dirname "$(realpath "$GH_WEBHOOK_SCRIPT_FILE")"`
The `FILENAME` will be determined by `basename "$(realpath "$GH_WEBHOOK_SCRIPT_FILE")"`
```bash
#!/bin/bash

# Stop at any failure
set -e

INTERPRETOR_COMMAND=`determine_interpretor_command`

if [ -z "$INTERPRETOR_COMMAND" ]; then
    echo "Failed to determine interpretor command for $GH_WEBHOOK_SCRIPT_INTERPRETOR"
    exit 1
fi

DIR_LOCATION=`dirname "$(realpath "$GH_WEBHOOK_SCRIPT_FILE")"`
FILENAME=`basename "$(realpath "$GH_WEBHOOK_SCRIPT_FILE")"`

cd "$DIR_LOCATION" && "$INTERPRETOR_COMMAND" "$FILENAME"
```

## Interpretors supported
```txt
bash
python3
```

## Run native compiled binaries
Set the `SCRIPT_INTERPRETOR` as `native` and the script will be run as a normal executable.
Just make sure to compile the binary with the coresponding arch of your docker engine

## My interpretor is not supported!

Just open an issue and we can discuss how we could add yours too

For compiled language it could be defined by using templates on how a script should be deployed
