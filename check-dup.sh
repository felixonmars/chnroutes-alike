#!/bin/bash
cat chnroutes-alike.txt chnroutes-alike-degraded.txt eu-bad.txt | grep -v "^$" | sort | uniq -c -d
