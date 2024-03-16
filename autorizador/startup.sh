#!/bin/bash
rq worker -u 'redis://redis/0' &
python autorizador.py &
wait