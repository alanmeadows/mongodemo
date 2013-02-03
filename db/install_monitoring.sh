#!/bin/bash

wget -q https://www.serverdensity.com/downloads/boxedice-public.key -O- | sudo apt-key add -
rm -rf /etc/apt/sources.list.d/sd-agent.list
cat <<EOF>>/etc/apt/sources.list.d/sd-agent.list
deb http://www.serverdensity.com/downloads/linux/deb all main
EOF
sudo apt-get update
sudo apt-get -y install sd-agent rpl
rpl "sd_url: http://example.serverdensity.com" "sd_url: http://nephodemo.serverdensity.com" /etc/sd-agent/config.cfg
if ! grep -q cb0b5560fd618cd06b736d67df348f19 /etc/sd-agent/config.cfg;
then
   rpl "agent_key:" "agent_key: cb0b5560fd618cd06b736d67df348f19" /etc/sd-agent/config.cfg
fi;
easy_install pymongo
if ! grep -q "mongodb_server: mongodb://localhost" /etc/sd-agent/config.cfg;
then
    rpl "mongodb_server:" "mongodb_server: mongodb://localhost" /etc/sd-agent/config.cfg
    rpl "mongodb_dbstats: no" "mongodb_dbstats: yes" /etc/sd-agent/config.cfg
    rpl "mongodb_replset: no" "mongodb_replset: yes" /etc/sd-agent/config.cfg
fi;
sudo /etc/init.d/sd-agent start
