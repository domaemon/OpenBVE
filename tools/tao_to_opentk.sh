#!/usr/bin/env bash

for i in `find .. -name \*.cs`; do
    echo $i.tmp
    ./tao_to_opentk.py -i $i -o stdout > $i.tmp
    mv $i.tmp $i
done
