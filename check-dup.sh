#!/bin/bash
cat chnroutes-alike.txt | grep -v "^$" | sort | uniq -c -d
