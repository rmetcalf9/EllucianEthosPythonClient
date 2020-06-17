#!/bin/bash

echo 'To test one file pass filename as first param'
echo 'e.g. sudo ./continous_test.sh wip'

if [ $# -eq 0 ]; then
  until ack -f --python  ./EllucianEthosPythonClient ./tests | entr -d nosetests --rednose ./tests; do sleep 1; done
else
  echo "Only testing tagged - ${1}"
  until ack -f --python  ./EllucianEthosPythonClient ./tests | entr -d nosetests --rednose -a ${1}; do sleep 1; done
fi
