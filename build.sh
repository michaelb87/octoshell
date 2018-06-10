#!/bin/sh

virtualenv -ppython3 .env && . .env/bin/activate && pip install -r requirements.txt
