@echo off
python -m ensurepip --user --default-pip
python -m pip install --user -Ur requirements.txt pywin32 pip
