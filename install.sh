#!/bin/bash

# Define the user, hostname and directory path of the Raspberry Pi
user=mimir
hostname=mimir.local
dir_path=mimir

# Copy all the required Python files and directories to Raspberry Pi
scp -i ~/.ssh/id_rsa.pub ./*.py ${user}@${hostname}:~/${dir_path}/
scp -i ~/.ssh/id_rsa.pub ./sensors/*.py ${user}@${hostname}:~/${dir_path}/sensors/
scp -i ~/.ssh/id_rsa.pub ./model/*.py ${user}@${hostname}:~/${dir_path}/model/
scp -i ~/.ssh/id_rsa.pub ./server/*.py ${user}@${hostname}:~/${dir_path}/server/
scp -i ~/.ssh/id_rsa.pub ./config/*.mysql ${user}@${hostname}:~/${dir_path}/config/

# Check if --service flag is provided and copy over .service file if it is
if [ "$1" == "--service" ]; then
    scp -i ~/.ssh/id_rsa.pub mimir.service ${user}@${hostname}:~/${dir_path}/
fi