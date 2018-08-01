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
curl -L https://github.com/jgm/pandoc/releases/download/2.2.2.1/pandoc-2.2.2.1-1-amd64.deb -o ${OFILE}
dpkg -i ${OFILE}
rm -f ${OFILE}


