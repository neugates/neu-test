import random


import common.api as api
import common.config as config
import common.tag as ctag


def fins_gen_tag(area):
    address = random.randint(0, 256)
    attribute = config.NEU_TAG_ATTRIBUTE_RW
    type = ctag.random_type([
        config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16,
        config.NEU_TYPE_INT32, config.NEU_TYPE_UINT32,
        config.NEU_TYPE_INT64, config.NEU_TYPE_UINT64,
        config.NEU_TYPE_FLOAT, config.NEU_TYPE_DOUBLE,
        config.NEU_TYPE_BIT, config.NEU_TYPE_STRING])

    if area == 'CIO':
        address = 'CIO' + str(address)
    elif area == 'A':
        address = 'A' + str(address)
        attribute = config.NEU_TAG_ATTRIBUTE_READ
    elif area == 'W':
        address = 'W' + str(address)
    elif area == 'H':
        address = 'H' + str(address)
    elif area == 'D':
        address = 'D' + str(address)
    elif area == 'P':
        address = 'P' + str(address)
        if type == config.NEU_TYPE_BIT:
            attribute = config.NEU_TAG_ATTRIBUTE_READ
    elif area == 'F':
        type = ctag.random_type([config.NEU_TYPE_INT8, config.NEU_TYPE_UINT8])
        address = 'F' + str(address)
    elif area == 'EM':
        em_address = random.randint(0, 12)
        address = 'EM' + str(em_address) + str(address)

    n_byte = 0
    if type == config.NEU_TYPE_BIT:
        bit = random.randint(0, 15)
        address = address + '.' + str(bit)
    elif type == config.NEU_TYPE_STRING:
        length = random.randrange(10, 128, 2)
        address = address + '.' + str(length)
        n_byte = length

    return address, type, attribute, n_byte


def fins_node_setting(
    api: api.NeuronAPI,
    node: str,
    host: str,
    port: int,
    etype: int
) -> dict:
    return api.node_setting(
        node,
        json={
            "host": host,
            "port": port,
            "type": etype,
        },
    )
