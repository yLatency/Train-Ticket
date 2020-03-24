#!/usr/bin/env python
# coding: utf-8

import random
import json
import sys

CONFIG_JSON = "latency-injector/src/main/resources/config.json"
SYNC_RPCS_PATH = "syncRPCs.txt"
ASYNC_RPCS_PATH = "asyncRPCs.txt"

NUM_AFFECTED_CLASSES = int(sys.argv[1])
NUM_REQ_CLASSES = 10
NUM_NOISED_CLASSES = 5
MAX_AFFECTED_RPCS_WCLASS = 3

delay = lambda: 50


def read_rpcs(RPCS_PATH):
    with open(RPCS_PATH, mode='r') as f:
        rpcs = [url.replace('\n', '') for url in f.readlines()]
    return rpcs


def random_rpcs(rpcs):
    return sorted(random.sample(rpcs, k=random.randint(1, MAX_AFFECTED_RPCS_WCLASS)))


def select_affected_syncrpcs(rpcs):
    affected_rpcs = []
    while len(affected_rpcs) < NUM_AFFECTED_CLASSES:
        selected_rpcs = random_rpcs(rpcs)
        if selected_rpcs not in affected_rpcs:
            affected_rpcs.append(selected_rpcs)
    return affected_rpcs

def select_affected_asyncrpc(rpcs):
    return random.choice(rpcs)



def add_sync_rpcs(cfg, rpcs, affected_rpcs):
    for rpc in rpcs:
        cfg[rpc] = []
        for i in range(NUM_REQ_CLASSES):
            delay_ = delay() if len(affected_rpcs) > i and rpc in affected_rpcs[i] else 0
            cfg[rpc].append(delay_)
    return cfg

def add_async_rpcs(cfg, rpcs, affected_rpc):
    for rpc in rpcs:
        if rpc == affected_rpc:
            cfg[rpc] = [delay() if i < NUM_NOISED_CLASSES else 0 for i in range(NUM_REQ_CLASSES)]
        else:
            cfg[rpc] = [0 for i in range(NUM_REQ_CLASSES)]
    return cfg

def write_config(config):
    with open(CONFIG_JSON, mode='w') as f:
        json.dump(config, f, indent=3)


def main():
    syncrpcs = read_rpcs(SYNC_RPCS_PATH)
    asyncrpcs = read_rpcs(ASYNC_RPCS_PATH)
    affected_syncrpcs = select_affected_syncrpcs(syncrpcs)
    affected_asyncrpc = select_affected_asyncrpc(asyncrpcs)
    config = {}
    add_sync_rpcs(config, syncrpcs, affected_syncrpcs)
    add_async_rpcs(config, asyncrpcs, affected_asyncrpc)
    write_config(config)


if __name__ == "__main__":
    main()
