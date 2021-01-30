FROM tensorflow/tensorflow:2.4.1-gpu-jupyter

WORKDIR /usr/licenta

RUN git clone https://github.com/Soare-Robert-Daniel/diploma-de-licenta.git . && python -m pip install -U pip &&  pip install -r requirements.txt && pip install jupyter -U && pip install jupyterlab

CMD jupyter lab --ip=0.0.0.0 --port=8080 --allow-root

EXPOSE 8080