#!/usr/bin/python

import requests
data = requests.get("https://www.gstatic.com/ipranges/cloud.json")
prefixes = data.json()["prefixes"]
eu_prefixes = set()

for prefix in prefixes:
    if prefix["scope"].startswith("europe"):
        eu_prefixes.add(prefix["ipv4Prefix"])

print("\n".join(sorted(eu_prefixes)))
