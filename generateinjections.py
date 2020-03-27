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

## Request std during a 5min load test without injection
## load test params: (--c) 20 users (--r) 1 hatch rate (--run-time)  5 minutes 
## user waiting time: wait_time = between(1.0, 3.0) random waiting time between 1 seconds and 3 seconds
REQ_STD = 5.59

def random_delay(affected_rpcs):
    delay_ = random.uniform(2*REQ_STD, 3*REQ_STD)/len(affected_rpcs)
    return int(round(delay_))


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
    
    for i, affected_rpcs_  in enumerate(affected_rpcs):
        delay = random_delay(affected_rpcs_)
        for rpc in rpcs:
            if rpc in affected_rpcs_:
                cfg[rpc].append(delay)
            else:
                cfg[rpc].append(0)

    for i in range(len(affected_rpcs), NUM_REQ_CLASSES):
        for rpc in rpcs:
            cfg[rpc].append(0)

    return cfg

def add_async_rpcs(cfg, rpcs, affected_rpc):
    delay = int(round(random.uniform(2*REQ_STD, 3*REQ_STD)))
    for rpc in rpcs:
        if rpc == affected_rpc:
            cfg[rpc] = [delay if i < NUM_NOISED_CLASSES else 0 for i in range(NUM_REQ_CLASSES)]
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
