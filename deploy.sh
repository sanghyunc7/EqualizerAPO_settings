#!/bin/bash

# source venv_EAPO/bin/activate
python3 translator.py he1000se.txt
git add -A

commit_msg="push by deploy script"
if [ "$#" -gt 0 ]; then
    commit_msg="$@"
fi
git commit -m "$commit_msg"


