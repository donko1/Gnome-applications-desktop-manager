
#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    python3 -m venv venv --without-pip
	sudo apt-get install xclip
	sudo apt-get install python3-tk
	sudo apt install git

	PYTHON_VERSION=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
	PYTHON_VENV="python${PYTHON_VERSION:0:4}-venv"
	sudo apt install $PYTHON_VENV

	source venv/bin/activate
	curl https://bootstrap.pypa.io/get-pip.py | python
	pip3 install -r requirements.txt
fi
source venv/bin/activate
python3 app.py
