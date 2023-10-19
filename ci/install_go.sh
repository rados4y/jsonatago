#!/bin/sh

manual_install() {
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
    wget -q "$url" -O go.tar.gz
    tar -C /usr/local -xzf go.tar.gz
    echo 'export PATH="$PATH:/usr/local/go/bin"' >> $HOME/.profile
    source $HOME/.profile
    export PATH="/usr/local/go/bin:$PATH"
    export GOROOT=/usr/local/go
    export GOPATH="$HOME/go"
}

uname -a
cat /etc/os-release
if command -v apk > /dev/null; then
    apk update
    apk add wget
    apk add go
elif command -v apt-get > /dev/null; then
    apt-get update
    apt-get install -y wget
    apt-get install -y go
elif command -v yum > /dev/null; then
    yum -y update
    yum -y install wget
    yum -y install go
else
    echo "unsupported platform"
    exit 1
fi

if ! command -v go > /dev/null; then
    echo "Go not found, manual install"
    manual_install
fi

which go
go version