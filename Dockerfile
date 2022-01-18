FROM python:3.6.13

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN apt-get -y update && \
    apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*


# Install DLIB
RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.4' --single-branch https://github.com/davisking/dlib.git dlib/ 
    
# Copy updated makefile
COPY CMakeLists.txt ~/dlib/tools/python/CMakeLists.txt
    
RUN cd ~ && \
    cd dlib/ && \
    python3 setup.py install 
    #--yes USE_AVX_INSTRUCTIONS


# Install Flask
RUN cd ~ && \
    pip3 install flask


# Install Face-Recognition Python Library
RUN cd ~ && \
    pip3 install -r requirements.txt


# Start the web service
CMD cd /root/ && \
    python3 run.py