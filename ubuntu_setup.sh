#!/bin/sh

if ! command -v docker &> /dev/null
then
    echo "Install docker on Ubuntu distro"
    # Remove old versions
    sudo apt-get remove docker docker-engine docker.io containerd runc

    # Update the apt package index and install packages to allow `apt` to use a repository over HTTPS
    sudo apt-get update

    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common

    # Add Docker’s official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

    # Add repository
    sudo add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) \
        stable"

    # Install docker engine
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io

    echo "Check docker installation"
    sudo docker run hello-world    
fi
