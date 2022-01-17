wget https://repo.anaconda.com/archive/Anaconda3-5.3.1-Linux-x86_64.sh && echo yes |  bash Anaconda3-5.3.1-Linux-x86_64.sh && ./anaconda3/bin/conda init && conda create --name opencv-env-3.6.13 python=3.6.13 && conda activate opencv-env-3.6.13 && pip install -r requirements.txt --user && python run.py --host=0.0.0.0 --port=$PORT


