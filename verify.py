#!/usr/bin/python
import argparse
import asyncio
import ipaddress
import mtrpacket
import random
import socket
from termcolor import colored


def random_addr_in_range(range):
    network = ipaddress.ip_network(range)
    return str(network.network_address + random.randint(1, network.num_addresses - 2))


def read_networks(filename):
    networks = []
    # Only parse CN2 networks, ignore checking for others
    cn2flag = False
    with open(filename, "r") as f:
        for line in f:
            if "#" in line:
                if "CN2" in line:
                    cn2flag = True
                else:
                    cn2flag = False

            if "/" in line and not line.startswith("#") and cn2flag:
                networks.append(line.rstrip("\n"))
    return networks


local_addr = socket.gethostbyname(socket.gethostname())


async def probe(target, ttl):
    async with mtrpacket.MtrPacket() as mtr:
        return await mtr.probe(target, local_ip=local_addr, ttl=ttl)


async def check(network, ttlrange):
    target = random_addr_in_range(network)
    # TODO
    ttlrange = list(map(int, ttlrange.split("-")))
    for ttl in range(ttlrange[0], ttlrange[1] + 1):
        result = await probe(target, ttl)
        if result.responder and result.responder.startswith("59.43."):
            print(colored(f"{network} {target} CN2 detected: {result.responder}", "green"))
            return
    print(colored(f"{network} {target} no CN2 detected", "red"))


if __name__ == "__main__":
    description = "A simple verify library for chnroutes-alike"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-f', '--file', nargs='?', default="chnroutes-alike.txt", help="File to examine")
    parser.add_argument('-n', '--network', nargs='?', help="Check a network range.")
    parser.add_argument('-c', '--count', nargs='?', default=1, help="How many IP address to check in each range")
    parser.add_argument('-t', '--ttlrange', nargs='?', default="5-7", help="TTL to check")

    config = parser.parse_args()

    if config.network:
        networks = [config.network]
    else:
        networks = read_networks(config.file)

    loop = asyncio.get_event_loop()

    targets = []
    for network in networks:
        for _ in range(int(config.count)):
            targets.append(check(network, config.ttlrange))

    loop.run_until_complete(asyncio.wait(targets))
