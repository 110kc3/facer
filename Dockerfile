# FROM continuumio/miniconda3

# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# # Install DLIB
# RUN conda init

# RUN conda create --name conda-env python=3.6.13

# SHELL ["conda", "run", "--no-capture-output", "-n", "conda-env", "/bin/bash", "-c"]


# RUN pip install --upgrade pip
# RUN pip uninstall jwt
# RUN pip uninstall pyjwt
# RUN apt-get update
# RUN apt-get install -y python3-opencv
# RUN conda install -c conda-forge dlib
# RUN pip install cmake
# RUN pip install dlib
# RUN pip install -r requirements.txt --user

# # ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "conda-env", "python", "run.py"]
# # CMD exec python run.py
# # ENTRYPOINT ["/bin/bash"]
# # CMD [ "conda activate conda-env && python run.py" ]

# # ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "conda-env", "/bin/bash", "-c", "python", "run.py"]
# CMD conda run -n conda-env python run.py


# this one is working
# FROM python:3.6.13-slim-stretch

# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# # Install DLIB
# #RUN conda init

# #RUN conda create --name conda-env python=3.6.13

# #SHELL ["conda", "run", "--no-capture-output", "-n", "conda-env", "/bin/bash", "-c"]


# RUN pip install --upgrade pip
# RUN pip uninstall jwt
# RUN pip uninstall pyjwt
# RUN apt-get update -y
# # RUN apt-get install -y python3-opencv
# RUN pip install opencv-python
# RUN echo yes | apt install build-essential
# #RUN conda install -c conda-forge dlib
# RUN pip install cmake
# RUN pip install dlib
# RUN pip install -r requirements.txt --user

# # ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "conda-env", "python", "run.py"]
# # CMD exec python run.py
# # ENTRYPOINT ["/bin/bash"]
# # CMD [ "conda activate conda-env && python run.py" ]

# # ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "conda-env", "/bin/bash", "-c", "python", "run.py"]
# CMD  python run.py


FROM jeffbebe/python-3.6.13-facer

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install DLIB
#RUN conda init

#RUN conda create --name conda-env python=3.6.13

#SHELL ["conda", "run", "--no-capture-output", "-n", "conda-env", "/bin/bash", "-c"]


# RUN pip install --upgrade pip
# RUN pip uninstall jwt
# RUN pip uninstall pyjwt
# RUN apt-get update -y
# # RUN apt-get install -y python3-opencv
# RUN pip install opencv-python
# RUN echo yes | apt install build-essential
# #RUN conda install -c conda-forge dlib
# RUN pip install cmake
# RUN pip install dlib
RUN pip install -r requirements.txt --user

# ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "conda-env", "python", "run.py"]
# CMD exec python run.py
# ENTRYPOINT ["/bin/bash"]
# CMD [ "conda activate conda-env && python run.py" ]

# ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "conda-env", "/bin/bash", "-c", "python", "run.py"]
CMD  python run.py