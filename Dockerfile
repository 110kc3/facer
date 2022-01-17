# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.6.13

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

CMD wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86.sh
CMD echo yes | bash Anaconda3-5.3.1-Linux-x86.sh
CMD ./anaconda3/bin/conda init
CMD conda create --name opencv-env-3.6.13 python=3.6.13
CMD conda activate opencv-env-3.6.13
CMD pip install -r requirements.txt --user
CMD build -t us-central1-docker.pkg.dev/${PROJECT_ID}/${_REPO_NAME}/myimage:${SHORT_SHA} .,
CMD push us-central1-docker.pkg.dev/${PROJECT_ID}/${_REPO_NAME}/myimage:${SHORT_SHA}

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app