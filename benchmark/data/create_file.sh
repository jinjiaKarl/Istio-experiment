#!/bin/bash

for ((i = 0 ; i <= 5000 ; i += 500)); do
    if [ $i -eq 0 ]; then
        touch "100_no_sidecar.json"
        touch "100_sidecar.json"
    else
        touch "${i}_no_sidecar.json"
        touch "${i}_sidecar.json"
    fi
done