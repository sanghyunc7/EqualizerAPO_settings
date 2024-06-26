#!/bin/bash

# source venv_EAPO/bin/activate
python3 translator.py he1000se.txt
git add -A

commit_msg="push by deploy script"
if [ "$#" -gt 0 ]; then
    commit_msg="$@"
fi
git commit -m "$commit_msg"
git push origin master

ssh -t admin@raspberrypi.local << 'END_SCRIPT'

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
    git pull --ff-only
    cp *.yml /usr/share/camilladsp/configs/
    sudo systemctl restart mpd.service && mpc play
    echo "DONE"

    exit
    
END_SCRIPT


