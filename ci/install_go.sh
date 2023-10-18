#!/bin/bash

architecture=$(uname -m)

case $architecture in
    x86_64)
        echo "64-bit system detected"
        ;;
    i386|i486|i586|i686)
        echo "32-bit system detected"
        ;;
    *)
        echo "Unknown architecture detected: $architecture"
        ;;
esac

if command -v yum &> /dev/null
then
    architecture=$(uname -m)
    url=""
    case $architecture in
        x86_64)
            url="https://golang.org/dl/go1.18.linux-amd64.tar.gz"
            ;;
        i386|i486|i586|i686)
            url="https://go.dev/dl/go1.21.3.linux-386.tar.gz"
            ;;
        *)
            echo "Unknown architecture: $architecture"
            exit 1
            ;;
    esac
    yum -y update
    yum -y install wget
    wget -q "$url" -O go.tar.gz
    tar -C /usr/local -xzf go.tar.gz
    echo "export PATH=$PATH:/usr/local/go/bin" >> $HOME/.bash_profile
    source $HOME/.bash_profile
    export PATH=/usr/local/go/bin:$PATH
    export GOROOT=/usr/local/go
    export GOPATH=$HOME/go
    go version
    which go
    ls /usr/local/go/bin/
else
    echo "Unsupported OS - yum not available"
    exit 1
fi
