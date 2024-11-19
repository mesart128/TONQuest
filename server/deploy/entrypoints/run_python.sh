#!/bin/sh
echo "Starting scanner..."
#export PYTHONPATH=$PWD/server
#echo "PYTHONPATH set to $PYTHONPATH"
python --version
python server/server.py --reload
echo "Server script finished"