#!/bin/sh

# Volumul de baza unde dorim sa ne salvam datele
STORAGE=stocare

if ! command -v docker &> /dev/null
then
    echo "Docker nu este instalat"
    exit
fi

if [ ! "$( docker images licenta/programa:latest -q )" ]; then
    echo "Imaginea de baza nu este creata si anume: licenta/program:latest" 
    exit
fi

if [ ! "$( docker volume ls -q --filter name=$STORAGE )" ]; then
    echo "Creez un volum numit:" $STORAGE
    docker create volume $STORAGE
fi

echo "Pornesc containerul de dezvoltare pe portul 8080"
docker run -v $STORAGE:/usr/licenta -p 8080:8080 licenta/program:latest
