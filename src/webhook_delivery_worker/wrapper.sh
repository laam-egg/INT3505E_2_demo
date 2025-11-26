#!/bin/bash

python -m app master &

# 8 slave workers
python -m app slave &
python -m app slave &
python -m app slave &
python -m app slave &
python -m app slave &
python -m app slave &
python -m app slave &
python -m app slave &

wait -n

exit $?
