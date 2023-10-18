#!/bin/bash

# Function to determine the package manager
install_wget() {
    if command -v wget > /dev/null; then
        echo "wget is already installed"
    else
        if command -v apt-get > /dev/null; then
            apt-get update
            apt-get install -y wget
        elif command -v yum > /dev/null; then
            yum -y update
            yum -y install wget
        else
            echo "Neither apt-get nor yum are available"
            exit 1
        fi
    fi
}
install_wget

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
uname -a
wget -q "$url" -O go.tar.gz
tar -C /usr/local -xzf go.tar.gz
echo "export PATH=$PATH:/usr/local/go/bin" >> $HOME/.bash_profile
source $HOME/.bash_profile
export PATH=/usr/local/go/bin:$PATH
export GOROOT=/usr/local/go
export GOPATH=$HOME/go
go version
which go
