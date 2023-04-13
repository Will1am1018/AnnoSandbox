#!/bin/bash

# Copyright (C) 2014-2016 anno sandbox Foundation.
# Copyright (C) 2020-2021 PowerLZY.
# This file is part of anno sandbox Sandbox - 


FILEPATH=$(readlink -f ${0%})
FILEPATHDIR=$(dirname $FILEPATH)

cd /tmp/
python $FILEPATHDIR/agent.py >$FILEPATHDIR/agent.stdout 2>$FILEPATHDIR/agent.stderr &

