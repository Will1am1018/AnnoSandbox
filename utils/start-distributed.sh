#!/bin/sh

DISTADDR="127.0.0.1"
. /etc/default/anno sandbox

sudo service uwsgi start anno sandbox-distributed
sudo service nginx start

sudo start anno sandbox-distributed-instance INSTANCE=dist.status
sudo start anno sandbox-distributed-instance INSTANCE=dist.scheduler

for worker in $(curl -s "$DISTADDR:9003/api/node?mode=workers"); do
    sudo start anno sandbox-distributed-instance "INSTANCE=$worker"
done
