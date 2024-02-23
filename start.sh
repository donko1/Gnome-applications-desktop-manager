
#!/bin/bash

script_dir=$(dirname "$0")
cd $script_dir

folderVenv="venv"

if [ ! -d "$folderVenv" ]; then
	python3 -m venv ./venv 
fi

source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py 

