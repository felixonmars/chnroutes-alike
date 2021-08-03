#!/bin/bash
cat chnroutes-alike.txt chnroutes-alike-degraded.txt | grep -v "^$" | sort | uniq -c -d
