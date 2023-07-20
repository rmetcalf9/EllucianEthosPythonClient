#!/bin/bash

echo 'To test one file pass filename as first param'

if [ $# -eq 0 ]; then
  until ack -f --python  ./EllucianEthosPythonClient ./tests | entr -d python3 -m pytest; do sleep 1; done
fi
