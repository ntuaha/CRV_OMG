#!/bin/sh
wget http://data.taipei/bus/BUSDATA -O /home/CRVomg/Project/CRV_OMG/data/BUSDATA.gz
gzip -df /home/CRVomg/Project/CRV_OMG/data/BUSDATA.gz
python -O /home/CRVomg/Project/CRV_OMG/src/appendBusData.py /home/CRVomg/Project/CRV_OMG/data/BUSDATA f
date > /home/CRVomg/Project/CRV_OMG/log/run.log
