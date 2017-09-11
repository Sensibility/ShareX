#!/bin/bash

export FLASK_APP="main.py"
if [ "$1" == "debug" ]; then
    export FLASK_DEBUG=1
fi

python3 -m flask run