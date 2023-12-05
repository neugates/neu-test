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


def kepware_node_setting(
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
