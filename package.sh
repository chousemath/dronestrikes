#!/bin/bash -
#===============================================================================
#
#          FILE: package.sh
#
#         USAGE: ./package.sh
#
#   DESCRIPTION:
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (),
#  ORGANIZATION:
#       CREATED: 11/17/2019 16:45:43
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

cd .venv/lib/python3.7/site-packages/
zip -r ../../../../function.zip .
cd ../../../..
zip -g function.zip f.py
aws lambda update-function-code --function-name updateDronestrikes --zip-file fileb://function.zip
aws lambda update-function-code --function-name readDronestrikes --zip-file fileb://function.zip

