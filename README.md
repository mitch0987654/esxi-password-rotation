# esxi-password-rotation
Contains the execution script and a verification script written with python. These scripts interact with the password vault, Keeper to rotate local user passwords and keep them updated.


**For isolation ive run this in a python virtual environment

#setup a new python venv

python -m venv python-venv-routers

#active this virtual environment

.\Scripts\activate

#Install the required modules

pip install pyvmomi

pip install keepercommander


#Within this python-venv-routers directory create the two script files and modify them as necessary. We will also need to create the config.json file required for keeper
