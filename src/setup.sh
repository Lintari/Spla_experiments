#!/bin/bash
set -e

echo "Загрузка репозитория"
git clone https://github.com/EgorOrachyov/graph-bench.git

cd graph-bench


git submodule update --init --recursive


python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install gdown

python3 scripts/build_spla.py
python3 scripts/build_lagraph.py



echo "Загрузка датасетов"
gdown --id "14RHaC_Ze_qoeb2GuhXOkirVaTvkRlv35" -O datasets.zip


echo "Распаковка датасетов"
unzip datasets.zip -d dataset/    #папка dataset уже есть в репозитории graph-bench 
rm datasets.zip

python3 scripts/convert.py

echo "подготовка репозитория завершена"
ls -l dataset/