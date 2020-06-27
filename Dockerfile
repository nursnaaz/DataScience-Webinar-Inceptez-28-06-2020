FROM python:3.7-slim-stretch

COPY . /usr/src/app
WORKDIR /usr/src/app




RUN pip install Werkzeug Flask numpy scipy Keras  pillow h5py tensorflow 

RUN conda install opencv

EXPOSE 5000
CMD [ "python" , "app.py"]

