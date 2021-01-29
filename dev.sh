#!/bin/sh

# Volumul de baza unde dorim sa ne salvam datele
STORAGE=stocare

if ! command -v docker &> /dev/null
then
    echo "Docker is not installed"
    exit
fi

if [ ! "$( docker volume ls -q --filter name=$STORAGE )" ]; then
    echo "Creez un volum numit:" $STORAGE
    docker create volume $STORAGE
fi

echo "Run development container on port 8080"
docker run -v $STORAGE:/usr/licenta -p 8080:8080 licenta/program
