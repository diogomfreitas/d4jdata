#!/bin/bash
echo "Chart"

for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
do
    cd ~/
    echo Versão "$i"b
    ls ~/PycharmProjects/d4jdata/data/Chart/"$i"b/jaguar/.jaguar/matrix/ > ~/PycharmProjects/d4jdata/data/Chart/"$i"b/matrix-files
    ls ~/PycharmProjects/d4jdata/data/Chart/"$i"b/jaguar/.jaguar/spectra/ > ~/PycharmProjects/d4jdata/data/Chart/"$i"b/spectra-files
done