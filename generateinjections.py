#!/usr/bin/env python
# coding: utf-8

import random
import json
import sys

CONFIG_JSON = "latency-injector/src/main/resources/config.json"
RPCS_PATH = "RPCs.txt"

NUM_AFFECTED_CLASSES = int(sys.argv[1])
NUM_REQ_CLASSES = 10
MAX_AFFECTED_RPCS_WCLASS = 3

delay = lambda: 50


def read_rpcs():
    with open(RPCS_PATH, mode='r') as f:
        rpcs = [url.replace('\n', '') for url in f.readlines()]
    return rpcs


def random_rpcs(rpcs):
    return sorted(random.sample(rpcs, k=random.randint(1, MAX_AFFECTED_RPCS_WCLASS)))


def select_affected_rpcs(rpcs):
    affected_rpcs = []
    while len(affected_rpcs) < NUM_AFFECTED_CLASSES:
        selected_rpcs = random_rpcs(rpcs)
        if selected_rpcs not in affected_rpcs:
            affected_rpcs.append(selected_rpcs)
    return affected_rpcs



def create_config(rpcs, affected_rpcs):
    cfg = {}
    for rpc in rpcs:
        cfg[rpc] = []
        for i in range(NUM_REQ_CLASSES):
            delay_ = delay() if len(affected_rpcs) > i and rpc in affected_rpcs[i] else 0
            cfg[rpc].append(delay_)
    return cfg


def write_config(config):
    with open(CONFIG_JSON, mode='w') as f:
        json.dump(config, f, indent=3)


def main():
    rpcs = read_rpcs()
    affected_rpcs = select_affected_rpcs(rpcs)
    config = create_config(rpcs, affected_rpcs)
    write_config(config)


if __name__ == "__main__":
    main()
