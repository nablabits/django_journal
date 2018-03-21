#!/bin/sh
#This is an auto setup scrip assuming you have python3, pip and requierments.txt
python3 -m venv  && echo "environment created"
source venv/bin/activate && echo "env activated"
pip install --upgrade pip && echo "upgrading pìp"
pip install -r requirements.txt && echo "installed requirements"
echo "Done!"
