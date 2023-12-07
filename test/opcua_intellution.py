import logging
import random
import time
from typing import List

from locust import HttpUser, task, between

import common.api as api
import common.config as config
from common.opcua import opcua_node_setting, kepserver_tags, random_value


class IntellutionTest(HttpUser):
    wait_time = between(0.1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = api.NeuronAPI(self.client)
        self.tags = kepserver_tags(4000)
        random.shuffle(self.tags)

    def on_start(self):
        self.c.del_node("opcua_intellution")
        self.c.add_node("opcua_intellution", config.PLUGIN_OPCUA)
        self.c.add_group("opcua_intellution", "intellution", 3000)

        opcua_node_setting(
            self.c,
            node="opcua_intellution",
            url="opc.tcp://192.168.10.174:49310",
            username="",
            password="",
        )

        self.c.add_tags("opcua_intellution", "intellution", self.tags)

    def on_stop(self):
        self.c.stop_node("opcua_intellution")

    @task(10)
    def read_tags(self):
        with self.c.read_tags("opcua_intellution", "intellution") as response:
            response.request_meta["name"] = "opcua intellution read tags"
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

    @task(1)
    def write_tag(self):
        selected = random.sample(self.tags, 200)
        random_value(selected)
        for tag in selected:
            with self.c.write_tag(
                "opcua_intellution", "intellution", tag["name"], tag["value"]
            ) as response:
                pass

    @task(1)
    def write_tags(self):
        selected = random.sample(self.tags, 10)
        random_value(selected)
        with self.c.write_tags(
            "opcua_intellution",
            "intellution",
            [{"tag": tag["name"], "value": tag["value"]} for tag in selected],
        ) as response:
            pass
            #logging.info(response.status_code)
