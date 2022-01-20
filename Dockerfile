############### create jeffbebe/pyth-facer from this part####################################################################
# FROM python:3.6.13-slim-stretch

# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# RUN pip install --upgrade pip
# RUN pip uninstall jwt
# RUN pip uninstall pyjwt
# RUN apt-get update -y
# RUN pip install opencv-python
# RUN echo yes | apt install build-essential
# RUN pip install cmake
# RUN pip install dlib
# RUN echo yes | apt-get install -y libtk8.6 
# RUN apt-get install ffmpeg libsm6 libxext6  -y
# RUN pip install -r requirements.txt --user

# CMD exec python run.py


################ new one ########################
FROM jeffbebe/pyth-facer

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

CMD exec python run.py