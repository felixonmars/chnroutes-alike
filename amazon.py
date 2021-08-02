#!/usr/bin/python

import requests
data = requests.get("https://ip-ranges.amazonaws.com/ip-ranges.json")
prefixes = data.json()["prefixes"]
eu_prefixes = set()

for prefix in prefixes:
    if prefix["region"].startswith("eu") and prefix["service"] in ("EC2", "S3"):
        eu_prefixes.add(prefix["ip_prefix"])

print("\n".join(sorted(eu_prefixes)))
