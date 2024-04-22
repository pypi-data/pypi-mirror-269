#!/bin/sh

flake8 --exclude=.venv, .vvenv
python -m unittest discover -s tests