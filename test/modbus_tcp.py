import logging

from locust import HttpUser, task, between

import common.api as api
import common.config as config
import common.modbus as modbus


class ModbusTcpRandom(HttpUser):
    wait_time = between(0.1, 2)

    # random generation of tags

    def on_start(self):
        self.tags = []
        self.tags += modbus.random_hold_register_tag(100)
        self.c = api.NeuronAPI(self.client)
        self.c.del_node("modbus_tcp")
        self.c.add_node("modbus_tcp", config.PLUGIN_MODBUS_TCP)
        self.c.add_group("modbus_tcp", "group_1", 100)
        self.c.modbus_tcp_node_setting('modbus_tcp', '192.168.10.152', 5023)
        self.c.add_tags("modbus_tcp", "group_1", self.tags)

    def on_stop(self):
        self.c.stop_node("modbus_tcp")

    @task(10)
    def read_tags(self):
        with self.c.read_tags("modbus_tcp", "group_1") as response:
            response.request_meta['name'] = "modbus tcp read tags"
            if response.status_code == 200:
                tags = response.json()['tags']
                result = list(
                    filter(lambda tag: tag.get('value') is None, tags))
                if len(result) == 0:
                    response.success()
                else:
                   # logging.warning("read tags error" + str(result))
                    response.failure("read tags error")
            else:
                response.failure("Failed to read tags")

    @task(1)
    def write_tag(self):
        pass
        # TODO: write and read tag, check tag value

    @task(1)
    def write_tags(self):
        pass
        # TODO: write and read tags, check tag value


class ModbusTcpFixed(HttpUser):
    wait_time = between(0.1, 2)

    # fixed tags

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(10)
    def read_tags(self):
        pass
        # TODO: read tags, check tag value

    @task(1)
    def write_tag(self):
        pass

    @task(1)
    def write_tags(self):
        pass
