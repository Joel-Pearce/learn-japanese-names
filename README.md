# learn-japanese-names


## Setup
* Install Python 3.11

Check your python version starts with 3.11 i.e.
```
python --version

Python 3.11.2
```

### Create the virtual environment

From top level repo directory:

```
python -m venv .venv
```

...or if using PyCharm **when importing project**, create venv and set local python interpreter to use it:

In Pycharm:
1) File -> New Project... :
2) Select 'New environment using' -> Virtualenv
3) Set 'location' to top level of project folder
4) Base interpreter should be set to global Python install.


### Enter the virtual environment

...either macOS using bash/zsh:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

...or if using Pycharm, if venv not set up during project import:

1) settings -> project -> python interpreter -> add interpreter -> add local interpreter
2) **If not previously created** -> Environment -> New -> select path to top level of project
3) **If previously created** -> Environment -> Existing -> Select path to local venv/scripts/python.exe
4) Do not inherit global site packages

To check if Pycharm is running local interpreter (rather than global):

    pip -V    # check the resultant path points to virtual env folder in project

Add pip tools:
```
python -m pip install pip-tools
```

Install dependencies:
```
python -m pip install --upgrade pip && pip install -r requirements.txt
```
