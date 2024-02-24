
#!/bin/bash

script_dir=$(dirname "$0")
cd $script_dir

source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
