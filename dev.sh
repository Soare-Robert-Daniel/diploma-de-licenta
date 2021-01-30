#!/bin/sh

# Volumul de baza unde dorim sa ne salvam datele
STORAGE=stocare
NAME=dev_serv

if ! command -v docker &> /dev/null
then
    echo "Docker nu este instalat"
    exit
fi

if [ ! "$( docker images licenta/program:latest -q )" ]; then
    echo "Imaginea de baza nu este creata si anume: licenta/program:latest" 
    exit
fi

if [ ! "$( docker volume ls -q --filter name=$STORAGE )" ]; then
    echo "Creez un volum numit:" $STORAGE
    docker create volume $STORAGE
fi

if [ ! "$( docker ps -a | grep $NAME )" ]; then 
    echo "Pornesc containerul de dezvoltare: " $NAME " pe portul 8080"
    docker run -v $STORAGE:/usr/licenta -p 8080:8080 --name $NAME --gpus all licenta/program:latest
    exit
fi

echo "Repornesc containerul de dezvoltare: " $NAME " pe portul 8080"
docker restart $NAME


