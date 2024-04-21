#!/bin/bash

# Replace dot with escaped dot :)
version=${1//\./\\.}

sed -i "s/$version/dev/g" "web/src/beepy.js"
sed -i "s/$version/0.0a0/g" "beepy/framework.py"
