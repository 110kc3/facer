FROM continuumio/miniconda3

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install DLIB
RUN conda init

RUN conda create --name conda-env python=3.6.13

SHELL ["conda", "run", "--no-capture-output", "-n", "conda-env", "/bin/bash", "-c"]


RUN pip install --upgrade pip
RUN pip uninstall jwt
RUN pip uninstall pyjwt
RUN apt-get update
RUN apt-get install -y python3-opencv
RUN conda install -c conda-forge dlib
RUN pip install cmake
RUN pip install dlib
RUN pip install -r requirements.txt --user

CMD ["python", "run.py"]