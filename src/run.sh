#!/bin/bash
set -e

if [ -z "$1" ]; then
  exit 1
fi

REAL_USER=$SUDO_USER
GRAPHS=$(IFS=,; echo "$*")

sudo -u $REAL_USER python3 -m venv venv
sudo -u $REAL_USER venv/bin/pip install numpy scipy matplotlib


cd graph-bench

sudo -u $REAL_USER mkdir -p results_industrial

for i in {1..20}
do
    echo "тест $i из 20..."
    sync; echo 3 > /proc/sys/vm/drop_caches
    
    OUT_FILE="results_industrial/results_$i.csv"
    sudo -u $REAL_USER ../venv/bin/python3 scripts/benchmark.py --tool=spla,lagraph --csvall=$OUT_FILE --graph="$GRAPHS"
    echo "--------------------------------------------------"
done


sudo -u $REAL_USER ../venv/bin/python3 plot.py 

echo "тесты завершены"