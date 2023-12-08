import logging
import random
import time
from typing import List

from locust import HttpUser, task, between

import common.api as api
import common.config as config
from common.opcua import (
    opcua_node_setting,
    cct_tags,
    opcua_random_value,
    opcua_default_node,
    opcua_read_tags,
    opcua_write_tag,
    opcua_write_tags,
)

DEFAULT_TEST_NAME = "ua/cct"
DEFAULT_NODE_NAME = "opcua_cct"
DEFAULT_GROUP_NAME = "cct"
DEFAULT_URL = "opc.tcp://192.168.10.134:48402"


class CCTTest(HttpUser):
    wait_time = between(0.1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = api.NeuronAPI(self.client)
        self.tags = cct_tags()
        random.shuffle(self.tags)

    def on_start(self):
        opcua_default_node(
            api=self.c, node=DEFAULT_NODE_NAME, group=DEFAULT_GROUP_NAME, tags=self.tags
        )

        opcua_node_setting(
            api=self.c,
            node=DEFAULT_NODE_NAME,
            url=DEFAULT_URL,
        )

    def on_stop(self):
        self.c.stop_node(DEFAULT_NODE_NAME)

    @task(10)
    def read_tags(self):
        opcua_read_tags(
            api=self.c,
            test=DEFAULT_TEST_NAME,
            node=DEFAULT_NODE_NAME,
            group=DEFAULT_GROUP_NAME,
        )

    @task(1)
    def write_tag(self):
        selected = random.sample(self.tags, 10)
        opcua_random_value(selected)
        opcua_write_tag(
            api=self.c,
            test=DEFAULT_TEST_NAME,
            node=DEFAULT_NODE_NAME,
            group=DEFAULT_GROUP_NAME,
            selected=selected,
        )

    @task(1)
    def write_tags(self):
        selected = random.sample(self.tags, 10)
        opcua_random_value(selected)
        opcua_write_tags(
            api=self.c,
            test=DEFAULT_TEST_NAME,
            node=DEFAULT_NODE_NAME,
            group=DEFAULT_GROUP_NAME,
            selected=selected,
        )
