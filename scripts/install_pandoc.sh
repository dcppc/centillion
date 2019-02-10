#!/bin/bash
#
# for ubuntu 

if [ "$(id -u)" != "0" ]; then
    echo ""
    echo ""
    echo "This script should be run as root."
    echo ""
    echo ""
    exit 1;
fi

OFILE="/tmp/pandoc.deb"

#VERSION="2.2.2.1"
VERSION="2.6"

curl -L -O https://github.com/jgm/pandoc/releases/download/${VERSION}/pandoc-${VERSION}-1-amd64.deb -o ${OFILE}

dpkg -i ${OFILE}
rm -f ${OFILE}


