#!/bin/bash
mkdir -p images
mkdir -p data
tar -xvzf EHTC_FirstM87Results_Apr2019_csv.tgz -C data --strip-components=1
mkdir -p data/csv/converted
