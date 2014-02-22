#!/bin/bash

# Extract majors-list from data
cut -f5 dat.tsv > majors-list

# Update major normalization dictionar
cp mdict mdict.backup
python dict-auto.py mdict.backup majors-list mdict

# Translate majors in dat.tsv
cp dat.tsv dat.tsv.backup
python translate.py mdict dat.tsv.backup dat.tsv

# Run R Script to train and upload the model.
./train-and-upload.R
