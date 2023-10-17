#!/bin/bash

if command -v yum &> /dev/null
then
    yum -y update
    yum -y install wget
    wget https://golang.org/dl/go1.18.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.18.linux-amd64.tar.gz
    echo "export PATH=$PATH:/usr/local/go/bin" >> $HOME/.bash_profile
    source $HOME/.bash_profile
else
    echo "Unsupported OS - yum not available"
    exit 1
fi