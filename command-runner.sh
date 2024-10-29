#!/bin/bash
set -e

WEBHOOK_SCRIPT_FILE="$1"
WEBHOOK_SCRIPT_INTERPRETOR="$2"

if [ $# -ne 2 ]; then
    echo "Usage: $0 <script-file> <script-interpretor>"
    exit 1
fi

determine_interpretor() {
    local interpretor=`command -v $WEBHOOK_SCRIPT_INTERPRETOR`
    if [ -z "$interpretor" ]
        echo "Interpretor not found for file $WEBHOOK_SCRIPT_INTERPRETOR"
        exit 1
    fi
    echo "$interpretor"
}

if [ -z "$WEBHOOK_SCRIPT_FILE" ]; then
    echo "WEBHOOK_SCRIPT_FILE is not set"
    exit 1
fi

if [ -z "$WEBHOOK_SCRIPT_INTERPRETOR" ]; then
    echo "WEBHOOK_SCRIPT_INTERPRETOR is not set"
    exit 1
fi

INTERPRETOR_COMMAND=`determine_interpretor`
DIR_LOCATION=`dirname \`realpath "$WEBHOOK_SCRIPT_FILE\``
FILENAME=`basename "$WEBHOOK_SCRIPT_FILE"`

cd "$DIR_LOCATION"

if [ ! -f "$FILENAME" ]; then
    echo "File $FILENAME not found in $DIR_LOCATION"
    exit 1
fi

if [ "$INTERPRETOR_COMMAND" == "bash" ]; then
    bash -c "$FILENAME"
elif [ "$INTERPRETOR_COMMAND" == "python3" ]; then
    python3 "$FILENAME"
elif [ "$INTERPRETOR_COMMAND" == "python" ]; then
    python "$FILENAME"
elif [ "$INTERPRETOR_COMMAND" == "node" ]; then
    node "$FILENAME"
elif [ "$INTERPRETOR_COMMAND" == "perl" ]; then
    perl "$FILENAME"
elif [ "$ALLOW_UNSAFE_INTERPRETOR" == 1 ]; then
    escaped_filename=`echo "$FILENAME" | sed -e 's/[$\'"\\`]/\\&/g'`
    bash -c "$INTERPRETOR_COMMAND $escaped_filename"
else
    echo "Interpretor $INTERPRETOR_COMMAND not supported"
    echo "It may not be safe to allow the interpretor to run abritary code"
fi