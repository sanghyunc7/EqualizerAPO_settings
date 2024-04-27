#!/bin/bash

source venv_EAPO/bin/activate
git stash
git pull
git stash pop
git add -A
git commit -m "update"
git push origin master