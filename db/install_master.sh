#!/bin/bash

# ./install_master.sh <slave_ip> <slave_ip>
#
# This script takes two arguments, the IP addresses of each
# of the slave servers

easy_install pymongo
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
rm -rf /etc/apt/sources.list.d/10gen.list
cat <<EOF>/etc/apt/sources.list.d/10gen.list
deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen
EOF
sudo apt-get update
sudo apt-get -y install mongodb-10gen
if ! grep -q '# nephomaster' /etc/mongodb.conf;
then
    cat <<EOF>>/etc/mongodb.conf
# nephomaster
master = true
replSet = r0
EOF
fi;
sudo service mongodb restart
sleep 3
echo 'rs.initiate()' | mongo --shell
sleep 15
echo "rs.add('$1')" | mongo --shell
echo "rs.add('$2')" | mongo --shell

