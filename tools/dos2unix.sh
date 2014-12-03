#!/usr/bin/env bash

for i in `find .. -name \*.cs`; do
    echo $i.tmp
    dos2unix $i
done
