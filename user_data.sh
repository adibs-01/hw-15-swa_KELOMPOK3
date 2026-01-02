#!/bin/bash
yum update -y
yum install -y git python3-pip

git clone https://github.com/VladimirArtyom/hw-15-swa /home/ec2-user/app
cd /home/ec2-user/app

pip3 install -r requirements.txt

python3 main.py
