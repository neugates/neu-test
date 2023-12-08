import itertools
import time
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


def opcua_random_value(tags: List[dict]) -> None:
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


def opcua_value_equal(tag1: dict, tag2: dict, type: int) -> bool:
    if tag1.get("value", None) is None:
        return False

    if type == config.NEU_TYPE_FLOAT or type == config.NEU_TYPE_DOUBLE:
        return abs(tag1["value"] - tag2["value"]) < 0.001
    return tag1["value"] == tag2["value"]


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


def wincc_tags() -> List[dict]:
    return [
        {
            "name": "opc_ua_DATA_A",
            "address": "1!t|opc_ua_DATA_A",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_INT16,
        },
        {
            "name": "opc_ua_DATA_B",
            "address": "1!t|opc_ua_DATA_B",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_INT32,
        },
        {
            "name": "opc_ua_DATA_C",
            "address": "1!t|opc_ua_DATA_C",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_STRING,
        },
        {
            "name": "opc_ua_DATA_D0",
            "address": "1!t|opc_ua_DATA_D[0]",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_INT16,
        },
        {
            "name": "opc_ua_DATA_D1",
            "address": "1!t|opc_ua_DATA_D[1]",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_INT16,
        },
    ]


def s71200_tags() -> List[dict]:
    return [
        {
            "name": "v1-1",
            "address": "4!29",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_UINT16,
        },
        {
            "name": "v1-2",
            "address": "4!38",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_UINT16,
        },
        {
            "name": "v2-1",
            "address": "4!39",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_INT8,
        },
        {
            "name": "v2-2",
            "address": "4!30",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_STRING,
        },
        {
            "name": "v3-1",
            "address": "4!40",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_DOUBLE,
        },
        {
            "name": "v3-2",
            "address": "4!31",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_UINT16,
        },
        {
            "name": "v4-1",
            "address": "4!41",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_UINT32,
        },
        {
            "name": "v4-2",
            "address": "4!32",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_FLOAT,
        },
        {
            "name": "v5-1",
            "address": "4!42",
            "attribute": config.NEU_TAG_ATTRIBUTE_RW,
            "type": config.NEU_TYPE_UINT16,
        },
        {
            "name": "v5-2",
            "address": "4!33",
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


def opcua_read_check(
    api: api.NeuronAPI,
    test: str,
    node: str,
    group: str,
    selected: List[dict],
) -> dict:
    with api.read_tags(node, group) as response:
        response.request_meta["name"] = f"{test} read tags"
        if response.status_code == 200:
            tags = response.json()["tags"]
            result = list(
                filter(
                    lambda tag: tag["name"] in [t["name"] for t in selected],
                    tags,
                )
            )

            if len(result) == 0:
                response.failure("read tags error")
                return
            else:
                for r in result:
                    for s in selected:
                        if s["name"] == r["name"]:
                            if opcua_value_equal(r, s, s["type"]):
                                response.success()
                            else:
                                response.failure(f"write/read tag:{r['name']} error")
                                # logging.warning(
                                #     f"{test} check tag:{r['name']} error, write:{s['value']}, read:{r['value']}"
                                # )
        else:
            response.failure("Failed to read tags")


def opcua_default_node(
    api: api.NeuronAPI,
    node: str,
    group: str,
    tags: List[dict],
    interval: int = 100,
) -> None:
    api.del_node(node)
    api.add_node(node, config.PLUGIN_OPCUA)
    api.add_group(node, group, interval)
    api.add_tags(node, group, tags)


def opcua_read_tags(
    api: api.NeuronAPI,
    test: str,
    node: str,
    group: str,
) -> None:
    with api.read_tags(node, group) as response:
        response.request_meta["name"] = f"{test} read tags"
        if response.status_code == 200:
            tags = response.json()["tags"]
            result = list(filter(lambda tag: tag.get("value") is None, tags))
            if len(result) == 0:
                response.success()
            else:
                # logging.warning("read tags error" + str(result))
                response.failure("read tags error")
        else:
            response.failure("Failed to read tags")


def opcua_write_tag(
    api: api.NeuronAPI,
    test: str,
    node: str,
    group: str,
    selected: List[dict],
    timeout: float = 0.5,
) -> dict:
    for tag in selected:
        with api.write_tag(node, group, tag["name"], tag["value"]) as response:
            response.request_meta["name"] = f"{test} write tag"
            if response.status_code != 200:
                response.failure("Failed to write tag")
                logging.warning(
                    f"{test} write tag, code:{response.status_code}, error:{response.text}, tag:{tag}"
                )

                return

    time.sleep(timeout)
    opcua_read_check(api, test, node, group, selected)


def opcua_write_tags(
    api: api.NeuronAPI,
    test: str,
    node: str,
    group: str,
    selected: List[dict],
    timeout: float = 0.5,
) -> dict:
    with api.write_tags(
        node,
        group,
        [{"tag": tag["name"], "value": tag["value"]} for tag in selected],
    ) as response:
        response.request_meta["name"] = f"{test} write tags"
        if response.status_code != 200:
            response.failure("Failed to write tags")
            logging.warning(
                f"{test} write tags, code:{response.status_code}, error:{response.text}"
            )

            return

    time.sleep(timeout)
    opcua_read_check(api, test, node, group, selected)


if __name__ == "__main__":
    pass
    # gen = gen_kepserver_tags()
    # for row in gen:
    #     print(row)
