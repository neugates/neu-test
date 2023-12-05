import itertools
from typing import List
import os
import csv
import logging
import random

import common.api as api
import common.config as config

KEPSERVER_DEVICE_NAME = "test"
KEPSERVER_CHANNEL_NAME = "数据类型示例"
KEPSERVER_CSV = "kepserver.csv"


def kepserver_type(raw_type: str) -> int:
    if "Boolean" == raw_type:
        return config.NEU_TYPE_BOOL
    elif "Double" == raw_type:
        return config.NEU_TYPE_DOUBLE
    elif "DWord" == raw_type:
        return config.NEU_TYPE_UINT32
    elif "Float" == raw_type:
        return config.NEU_TYPE_FLOAT
    elif "Long" == raw_type:
        return config.NEU_TYPE_INT32
    elif "Short" == raw_type:
        return config.NEU_TYPE_INT16
    elif "Word" == raw_type:
        return config.NEU_TYPE_UINT16
    elif "String" == raw_type:
        return config.NEU_TYPE_STRING
    else:
        return config.NEU_TYPE_ERROR


def random_value(tags: List[dict]) -> None:
    for tag in tags:
        type = tag["type"]
        if type == config.NEU_TYPE_INT16:
            value = random.randint(-32768, 32767)
        elif type == config.NEU_TYPE_UINT16:
            value = random.randint(0, 65535)
        elif type == config.NEU_TYPE_INT32:
            value = random.randint(-2147483648, 2147483647)
        elif type == config.NEU_TYPE_UINT32:
            value = random.randint(0, 4294967295)
        elif type == config.NEU_TYPE_FLOAT:
            value = random.uniform(-500.00, 500.00)
        elif type == config.NEU_TYPE_DOUBLE:
            value = random.uniform(-1000.00, 1000.00)
        elif type == config.NEU_TYPE_BOOL:
            value = random.randint(0, 1)
        elif type == config.NEU_TYPE_STRING:
            value = "hello" + str(random.randint(0, 65535))
        elif type == config.NEU_TYPE_INT64:
            value = random.randint(-9223372036854775808, 9223372036854775807)
        elif type == config.NEU_TYPE_UINT64:
            value = random.randint(0, 18446744073709551615)
        elif type == config.NEU_TYPE_INT8:
            value = random.randint(-128, 127)
        elif type == config.NEU_TYPE_UINT8:
            value = random.randint(0, 255)
        else:
            continue

        tag["value"] = value


def gen_kepserver_tags() -> dict:
    current_file_path = os.path.abspath(__file__)
    parent_directory_path = os.path.dirname(current_file_path)
    data_directory_path = os.path.join(
        parent_directory_path, f"../data/{KEPSERVER_CSV}"
    )
    with open(
        data_directory_path, mode="r", newline="", encoding="utf_8_sig"
    ) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        for i, row in enumerate(reader):
            yield {
                "name": row[1],
                "address": f"2!{KEPSERVER_CHANNEL_NAME}.{KEPSERVER_DEVICE_NAME}.{row[0]}",
                "attribute": config.NEU_TAG_ATTRIBUTE_RW,
                "type": kepserver_type(row[2]),
                "description": row[15],
                "decimal": 0,
                "precision": 0,
            }


def kepserver_tags(num: int) -> List[dict]:
    num_rows = num if num <= 4000 else 4000
    gen = gen_kepserver_tags()
    return list(itertools.islice(gen, num_rows))


def cct_tags() -> List[dict]:
    tags = []
    cct_bool = {
        "name": "s_bool",
        "address": "1!ft.type_bool",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_BOOL,
    }
    tags.append(cct_bool)

    cct_int8 = {
        "name": "s_int8",
        "address": "1!ft.type_int8",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT8,
    }
    tags.append(cct_int8)

    cct_uint8 = {
        "name": "s_uint8",
        "address": "1!ft.type_uint8",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT8,
    }
    tags.append(cct_uint8)

    cct_int16 = {
        "name": "s_int16",
        "address": "1!ft.type_int16",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT16,
    }
    tags.append(cct_int16)

    cct_uint16 = {
        "name": "s_uint16",
        "address": "1!ft.type_uint16",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT16,
    }
    tags.append(cct_uint16)

    cct_int32 = {
        "name": "s_int32",
        "address": "1!ft.type_int32",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT32,
    }
    tags.append(cct_int32)

    cct_uint32 = {
        "name": "s_uint32",
        "address": "1!ft.type_uint32",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT32,
    }
    tags.append(cct_uint32)

    cct_int64 = {
        "name": "s_int64",
        "address": "1!ft.type_int64",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT64,
    }
    tags.append(cct_int64)

    cct_uint64 = {
        "name": "s_uint64",
        "address": "1!ft.type_uint64",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT64,
    }
    tags.append(cct_uint64)

    cct_float = {
        "name": "s_float",
        "address": "1!ft.type_float",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_FLOAT,
    }
    tags.append(cct_float)

    cct_double = {
        "name": "s_double",
        "address": "1!ft.type_double",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_DOUBLE,
    }
    tags.append(cct_double)

    cct_string = {
        "name": "s_string",
        "address": "1!ft.type_cstr",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_STRING,
    }
    tags.append(cct_string)

    # cct_datetime = {
    #     "name": "i_datetime",
    #     "address": "0!2258",
    #     "attribute": config.NEU_TAG_ATTRIBUTE_READ,
    #     "type": config.NEU_TYPE_UINT32,
    # }
    # tags.append(cct_datetime)

    cct_guid_bool = {
        "name": "guid_bool",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae02",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_BOOL,
    }
    tags.append(cct_guid_bool)

    cct_guid_int8 = {
        "name": "guid_int8",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae00",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT8,
    }
    tags.append(cct_guid_int8)

    cct_guid_uint8 = {
        "name": "guid_uint8",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae01",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT8,
    }
    tags.append(cct_guid_uint8)

    cct_guid_int16 = {
        "name": "guid_int16",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae03",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT16,
    }
    tags.append(cct_guid_int16)

    cct_guid_uint16 = {
        "name": "guid_uint16",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae04",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT16,
    }
    tags.append(cct_guid_uint16)

    cct_guid_int32 = {
        "name": "guid_int32",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae05",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT32,
    }
    tags.append(cct_guid_int32)

    cct_guid_uint32 = {
        "name": "guid_uint32",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae06",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT32,
    }
    tags.append(cct_guid_uint32)

    cct_guid_int64 = {
        "name": "guid_int64",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae07",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_INT64,
    }
    tags.append(cct_guid_int64)

    cct_guid_uint64 = {
        "name": "guid_uint64",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae08",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_UINT64,
    }
    tags.append(cct_guid_uint64)

    cct_guid_float = {
        "name": "guid_float",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae09",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_FLOAT,
    }
    tags.append(cct_guid_float)

    cct_guid_double = {
        "name": "guid_double",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae0a",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_DOUBLE,
    }
    tags.append(cct_guid_double)

    cct_guid_string = {
        "name": "guid_string",
        "address": "1!c496578a-0dfe-4b8f-870a-745238c6ae0b",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_STRING,
    }
    tags.append(cct_guid_string)

    # cct_feak_guid_string = {
    #     "name": "feak_guid_cstr",
    #     "address": "1!c496578a0dfe4b8f870a745238c6ae0b----",
    #     "attribute": config.NEU_TAG_ATTRIBUTE_RW,
    #     "type": config.NEU_TYPE_STRING,
    # }
    # tags.append(cct_feak_guid_string)

    cct_numeric_id_string = {
        "name": "numeric_id_cstr",
        "address": "1!1234567",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_STRING,
    }
    tags.append(cct_numeric_id_string)

    # cct_unsupported_type = {
    #     "name": "unsupported_type",
    #     "address": "0!2260",
    #     "attribute": config.NEU_TAG_ATTRIBUTE_RW,
    #     "type": config.NEU_TYPE_STRING,
    # }
    # tags.append(cct_unsupported_type)

    # cct_not_good_address = {
    #     "name": "not_good_address",
    #     "address": "1!neu.not_good",
    #     "attribute": config.NEU_TAG_ATTRIBUTE_RW,
    #     "type": config.NEU_TYPE_STRING,
    # }
    # tags.append(cct_not_good_address)

    cct_ptr_string = {
        "name": "ptr_cstr",
        "address": "1!large_string",
        "attribute": config.NEU_TAG_ATTRIBUTE_RW,
        "type": config.NEU_TYPE_STRING,
    }
    tags.append(cct_ptr_string)

    return tags


def prosys_tags() -> List[dict]:
    return [
        {
            "name": "constant",
            "address": "3!1001",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_DOUBLE,
        },
        {
            "name": "counter",
            "address": "3!1002",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_INT32,
        },
        {
            "name": "random",
            "address": "3!1003",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_DOUBLE,
        },
        {
            "name": "sawtooth",
            "address": "3!1004",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_DOUBLE,
        },
        {
            "name": "sinusoid",
            "address": "3!1005",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_DOUBLE,
        },
        {
            "name": "square",
            "address": "3!1006",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_DOUBLE,
        },
        {
            "name": "triangle",
            "address": "3!1007",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_DOUBLE,
        },
    ]


def opcua_node_setting(
    api: api.NeuronAPI,
    node: str,
    url: str = "opc.tcp://localhost:4840",
    username: str = "",
    password: str = "",
    cert: str = "",
    key: str = "",
) -> dict:
    return api.node_setting(
        node,
        json={
            "url": url,
            "username": username,
            "password": password,
            "cert": cert,
            "key": key,
        },
    )


if __name__ == "__main__":
    gen = gen_kepserver_tags()
    for row in gen:
        print(row)
