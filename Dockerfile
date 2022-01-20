############### create jeffbebe/pyth-facer from this part####################################################################
# FROM python:3.6.13-slim-stretch

# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY requirements.txt ./

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

ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN echo y | pip uninstall gunicorn
#RUN pip install --no-cache-dir -r requirements.txt

RUN echo y | pip uninstall gunicorn 

#ENTRYPOINT [ "/bin/bash", "-c" ]
#CMD python --version
CMD exec  gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
#CMD ["gunicorn"  , "--bind", "0.0.0.0:8000", "app:app"]
