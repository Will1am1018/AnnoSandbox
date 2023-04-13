#!/bin/sh

DISTADDR="127.0.0.1"
. /etc/default/anno sandbox

for worker in $(curl -s "$DISTADDR:9003/api/node?mode=workers"); do
    sudo stop anno sandbox-distributed-instance "INSTANCE=$worker"
done

sudo stop anno sandbox-distributed-instance INSTANCE=dist.status
sudo stop anno sandbox-distributed-instance INSTANCE=dist.scheduler

sudo service uwsgi stop anno sandbox-distributed
sudo service nginx stop
