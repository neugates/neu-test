import random

import common.config as config
import common.api as api


types = [config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16,
         config.NEU_TYPE_INT32, config.NEU_TYPE_UINT32,
         config.NEU_TYPE_FLOAT, config.NEU_TYPE_INT64,
         config.NEU_TYPE_UINT64, config.NEU_TYPE_DOUBLE,
         config.NEU_TYPE_BIT, config.NEU_TYPE_STRING, config.NEU_TYPE_BYTES]


def modbus_gen_hold_register_tag(size=1):
    tags = []
    for index in range(size):
        address = random.randint(1, 3000)
        address = '1!4' + str(address)
        type = types[random.randint(0, len(types) - 1)]
        attribute = config.NEU_TAG_ATTRIBUTE_RW

        n_byte = 0
    if type == config.NEU_TYPE_BIT:
        bit = random.randint(0, 15)
        address = address + '.' + str(bit)
        attribute = config.NEU_TAG_ATTRIBUTE_READ
    elif type == config.NEU_TYPE_STRING:
        length = random.randrange(10, 128, 2)
        address = address + '.' + str(length)
        n_byte = length
    elif type == config.NEU_TYPE_BYTES:
        length = random.randrange(10, 128, 2)
        address = address + '.' + str(length)
        n_byte = length

        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": attribute,
            "type": type,
            "length": n_byte
        }

        tags.append(tag)
    return address, type, attribute, n_byte


def modbus_gen_input_register_tag(size=1):
    tags = []
    for index in range(size):
        address = random.randint(1, 3000)
        address = '1!3' + str(address)
        type = types[random.randint(0, len(types) - 1)]
        attribute = config.NEU_TAG_ATTRIBUTE_READ

        n_byte = 0
    if type == config.NEU_TYPE_BIT:
        bit = random.randint(0, 15)
        address = address + '.' + str(bit)
    elif type == config.NEU_TYPE_STRING:
        length = random.randrange(10, 128, 2)
        address = address + '.' + str(length)
        n_byte = length
    elif type == config.NEU_TYPE_BYTES:
        length = random.randrange(10, 128, 2)
        address = address + '.' + str(length)
    elif type == config.NEU_TYPE_INT16 or config.NEU_TYPE_UINT16:
        n_byte = 2
    elif type == config.NEU_TYPE_INT32 or config.NEU_TYPE_UINT32 or config.NEU_TYPE_FLOAT:
        n_byte = 4
    elif type == config.NEU_TYPE_INT64 or config.NEU_TYPE_UINT64 or config.NEU_TYPE_DOUBLE:
        n_byte = 8

        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": attribute,
            "type": type,
            "length": n_byte
        }

        tags.append(tag)
    return address, type, attribute, n_byte


def modbus_gen_coil_tag(size=1):
    tags = []
    for index in range(size):
        address = random.randint(1, 3000)
        address = '1!0' + str(address)
        type = config.NEU_TYPE_BIT
        attribute = config.NEU_TAG_ATTRIBUTE_RW

        n_byte = 1
        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": attribute,
            "type": type,
            "length": n_byte
        }

        tags.append(tag)
    return address, type, attribute, n_byte


def modbus_gen_input_tag(size=1):
    tags = []
    for index in range(size):
        address = random.randint(1, 3000)
        address = '1!1' + str(address)
        type = config.NEU_TYPE_BIT
        attribute = config.NEU_TAG_ATTRIBUTE_READ

        n_byte = 1
        tag = {
            "name": api.random_tag_name(),
            "address": address,
            "attribute": attribute,
            "type": type,
            "length": n_byte
        }

        tags.append(tag)
    return address, type, attribute, n_byte


def modbus_gen_fixed_tags():
    fixed_tags = [
        {"name": "hold_bit", "address": "1!400001.15", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_BIT, "v": 1},
        {"name": "hold_int16", "address": "1!400001", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_INT16, "v": 1},
        {"name": "hold_uint16", "address": "1!400002", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_UINT16, "v": 1},
        {"name": "hold_int32", "address": "1!400003", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_INT32, "v": 1},
        {"name": "hold_uint32", "address": "1!400015", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_UINT32, "v": 1},
        {"name": "hold_float", "address": "1!400017", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_FLOAT, "v": 1},
        {"name": "hold_string", "address": "1!400020.10", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_STRING, "v": "1"},
        {"name": "hold_bytes", "address": "1!400040.10", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_BYTES, "v": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},

        {"name": "input_register_bit", "address": "1!30101.15", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_BIT},
        {"name": "input_register_int16", "address": "1!30101", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_INT16},
        {"name": "input_register_uint16", "address": "1!30102", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_UINT16},
        {"name": "input_register_int32", "address": "1!30103", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_INT32},
        {"name": "input_register_uint32", "address": "1!30115", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_UINT32},
        {"name": "input_register_float", "address": "1!30117", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_FLOAT},
        {"name": "input_register_string", "address": "1!30120.10", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_STRING},
        {"name": "input_register_bytes", "address": "1!30130.10", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_BYTES},

        {"name": "coil_bit_1", "address": "1!000001", "attribute": config.NEU_TAG_ATTRIBUTE_RW, "type": config.NEU_TYPE_BIT, "v": 1},

        {"name": "input_bit_1", "address": "1!100001", "attribute": config.NEU_TAG_ATTRIBUTE_READ, "type": config.NEU_TYPE_BIT}
    ]
    return fixed_tags