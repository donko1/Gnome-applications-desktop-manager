#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


# Create the gnome_applications_manager executable in /bin if it doesn't exist
if [ ! -f /bin/gnome_applications_manager ]; then
    echo '#!/bin/bash' > /bin/gnome_applications_manager
    echo "exec '$SCRIPT_DIR/start.sh'" >> /bin/gnome_applications_manager
    chmod +x /bin/gnome_applications_manager
fi

cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv --without-pip
	sudo apt-get install xclip
	sudo apt-get install python3-tk
	sudo apt-get install curl
	
	PYTHON_VERSION=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
	PYTHON_VENV="python${PYTHON_VERSION:0:4}-venv"
	sudo apt install $PYTHON_VENV

    source venv/bin/activate
    curl https://bootstrap.pypa.io/get-pip.py | python
	pip3 install -r requirements.txt
	python3 settings.py
	chmod 666 settings.json 
fi

chmod +x start.sh

echo 'Nice! Now u can write "gnome_applications_manager" to start the app!'
