#!/bin/bash

echo "Removing old utf8-directory if present"
rm -rf utf8 
echo "Creating new directory, a processed copy of the files will be stored here"
mkdir utf8

echo "Converting UTF-16LE JSON-files to UTF-8"
for file in *.json;do echo "Processing" $file;iconv -f UTF-16LE -t UTF-8 $file -o utf8/$file;done

echo "Processing files. (POPing certain keys, adding some fields and removing BOM)"
for file in utf8/*.json; do python3 processing.py utf8/$file;done

echo "Done converting and processing."
