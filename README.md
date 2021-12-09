# facer

face_detector_only.py uses Stump-based 24x24 discrete adaboost frontal face detector.
haarcascade_frontalface_default.xml file for face detection

## Prerequisites for local usage

Use Conda - working every time

Instalation:

https://learnopencv.com/install-opencv-3-and-dlib-on-windows-python-only/

Commands:

conda create --name opencv-env-3.6.13 python=3.6.13

conda init powershell #(for windows powershell usage)

conda activate opencv-env-3.6.13

pip install -r requirements.txt

python run.py

To leave conda virtual environment:

conda deactivate

You could also use virtualenv - but it requires Python 3.6.13 exacly

1. Installing python/pip

https://www.python.org/downloads/

Install Python 3.6, some packages do not work on newer versions.

Add Python to the Windows Path
https://geek-university.com/python/add-python-to-the-windows-path/

Install pip

python -m pip install --upgrade pip

2. Install virtual environment

pip install virtualenv

3. Run flask server locally

Run only first time:

virtualenv env

env\scripts\activate

pip install -r requirements.txt

python run.py

Run every time you want to start the server:

env\scripts\activate

python run.py

## Noticed errors with instalation - caused by Python version > 3.6

ERROR: CMake must be installed to build dlib

or ERROR: Failed building wheel for dlib

1st workaround:

pip install cmake

pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f

2nd workaround:

Install Python 3.6.13

To reset the users and images table, run the following python script:

```
python init_db.py
```
