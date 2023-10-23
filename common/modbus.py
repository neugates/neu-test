import random
import string

import config
import api


types = [config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16,
         config.NEU_TYPE_INT32, config.NEU_TYPE_UINT32,
         config.NEU_TYPE_FLOAT, config.NEU_TYPE_INT64,
         config.NEU_TYPE_UINT64, config.NEU_TYPE_DOUBLE,
         config.NEU_TYPE_BIT, config.NEU_TYPE_STRING, config.NEU_TYPE_BYTES]


def random_hold_register_tag(size=1):
    tags = []

    for index in range(0, size):
        address = random.randint(1, 3000)
        address = '1!4' + str(address)
        type = types[random.randint(0, len(types) - 1)]

        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": type
        }

        if tag['type'] == config.NEU_TYPE_BIT:
            bit = random.randint(0, 15)
            tag["address"] = address + '.' + str(bit)
            tag['attribute'] = config.NEU_TAG_ATTRIBUTE_READ
        elif tag['type'] == config.NEU_TYPE_STRING:
            length = random.randrange(10, 128, 2)
            tag['address'] = address + '.' + str(length)
        elif tag['type'] == config.NEU_TYPE_BYTES:
            length = random.randrange(10, 128, 2)
            tag['address'] = address + '.' + str(length)

        tags.append(tag)

    return tags


def random_input_register_tag(size=1):
    tags = []

    for index in range(0, size):
        address = random.randint(1, 3000)
        address = '1!3' + str(address)
        type = types[random.randint(0, len(types) - 1)]

        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": config.NEU_TAG_ATTRIBUTE_READ,
            "type": type
        }

        if tag['type'] == config.NEU_TYPE_BIT:
            bit = random.randint(0, 15)
            tag["address"] = address + '.' + str(bit)
        elif tag['type'] == config.NEU_TYPE_STRING:
            length = random.randrange(10, 128, 2)
            tag['address'] = address + '.' + str(length)
        elif tag['type'] == config.NEU_TYPE_BYTES:
            length = random.randrange(10, 128, 2)
            tag['address'] = address + '.' + str(length)

        tags.append(tag)

    return tags


def random_coil_tag(size=1):
    tags = []

    for index in range(0, size):
        address = random.randint(1, 3000)
        address = '1!0' + str(address)

        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type":  config.NEU_TYPE_BIT
        }

        tags.append(tag)

    return tags


def random_input_tag(size=1):
    tags = []

    for index in range(0, size):
        address = random.randint(1, 3000)
        address = '1!0' + str(address)

        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": config.NEU_TAG_ATTRIBUTE_READ,
            "type":  config.NEU_TYPE_BIT
        }

        tags.append(tag)

    return tags
