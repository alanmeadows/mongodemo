#!/bin/bash

# ./install_slave.sh <master_ip>
#
# This script takes a single argument: the IP address
# of the mongo master server.  It assumes hosts entries
# have been already setup for the other various replica
# members

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
rm -rf /etc/apt/sources.list.d/10gen.list
cat <<EOF>/etc/apt/sources.list.d/10gen.list
deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen
EOF
sudo apt-get update
sudo apt-get -y install mongodb-10gen
if ! grep -q '# nephoslave' /etc/mongodb.conf;
then
    cat <<EOF>>/etc/mongodb.conf
# nephoslave
slave = true
source = $1
replSet = r0
EOF
fi;
sudo service mongodb restart

