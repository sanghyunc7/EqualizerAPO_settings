#!/bin/bash

source venv_EAPO/bin/activate
git stash
git pull
git stash pop
git add -A
git commit -m "push by deploy script"
git push origin master


ssh raspberrypi.local

target_dir="/home/admin/EqualizerAPO_settings"
if [ ! -d "$target_dir" ]; then
  echo "Directory $target_dir does not exist. Cloning..."
  git clone https://github.com/sanghyunc7/EqualizerAPO_settings.git "$target_dir"
  if [ $? -ne 0 ]; then
    echo "Error: Git clone failed!"
    exit 1
  fi
fi

cd "$target_dir"
git stash && git stash drop
git pull
cp he1000se.yml /usr/share/camilladsp/configs/

exit