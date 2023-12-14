from locust import HttpUser, task, between
import time
import logging
import common.api as api
import common.config as config
import common.modbus as modbus
import common.tag as ctag

class ModbusTcpRandom(HttpUser):
    wait_time = between(0.1, 2)

    def on_start(self):
        self.node_name = "modbus_tcp_random"
        self.group_name = "group_random"
        self.tags = []
        self.tags += ctag.random_tag(modbus.modbus_gen_hold_register_tag, 100)
        self.tags += ctag.random_tag(modbus.modbus_gen_input_register_tag, 50)
        self.tags += ctag.random_tag(modbus.modbus_gen_coil_tag, 100)
        self.tags += ctag.random_tag(modbus.modbus_gen_input_tag, 50)
        self.map_tags = {}
        for tag in self.tags:
            self.map_tags[tag['name']] = tag

        self.c = api.NeuronAPI(self.client)
        self.c.del_node(self.node_name)
        self.c.add_node(self.node_name, config.PLUGIN_MODBUS_TCP)
        self.c.add_group(self.node_name, self.group_name, 100)
        self.c.modbus_tcp_node_setting(self.node_name, '192.168.10.152', 5023)
        self.c.add_tags(self.node_name, self.group_name, self.tags)

    def on_stop(self):
        self.c.stop_node(self.node_name)

    @task(10)
    def read_tags(self):
        request_name = "modbus tcp random read tags"
        ctag.read_and_check(self.c,
                            request_name, self.node_name, self.group_name)

    @task(1)
    def write_tag(self):
        request_name = "modbus tcp random write tag"
        ctag.write_and_check(self.c, self.tags, self.map_tags,
                             request_name, self.node_name, self.group_name)

    @task(1)
    def write_tags(self):
        request_name = "modbus tcp random write multiple tags"
        write_multiple_tags = ctag.prepare_multiple_write_tags(self.tags)
        ctag.write_tags_and_check(self.c, write_multiple_tags, self.map_tags,
                             request_name, self.node_name, self.group_name)


class ModbusTcpFixed(HttpUser):
    wait_time = between(0.1, 2)

    def on_start(self):
        self.node_name = "modbus_tcp_fixed"
        self.group_name = "group_fixed"
        self.tags = modbus.modbus_gen_fixed_tags()
        self.map_tags = {tag['name']: tag for tag in self.tags}

        self.c = api.NeuronAPI(self.client)
        self.c.del_node(self.node_name)
        self.c.add_node(self.node_name, config.PLUGIN_MODBUS_TCP)
        self.c.add_group(self.node_name, self.group_name, 100)
        self.c.modbus_tcp_node_setting(self.node_name, '192.168.10.152', 5023)
        self.c.add_tags(self.node_name, self.group_name, self.tags)

    def on_stop(self):
        self.c.stop_node(self.node_name)

    @task(10)
    def read_tags(self):
        request_name = "modbus tcp fixed read tags"
        ctag.read_and_check(self.c,
                            request_name, self.node_name, self.group_name)

    @task(1)
    def write_tag(self):
        request_name = "modbus tcp fixed write tag"
        for tag in self.tags:
            if tag['attribute'] == config.NEU_TAG_ATTRIBUTE_RW:
                ctag.fixed_write_and_check(self.c, self.node_name, self.group_name, self.map_tags, tag, request_name)

    @task(1)
    def write_tags(self):
        request_name = "modbus tcp fixed write multiple tags"
        tags_data = [
            {"tag": tag['name'], "value": tag['v']}
            for tag in self.tags
            if tag['attribute'] == config.NEU_TAG_ATTRIBUTE_RW
        ]

        ctag.fixed_write_multiple_tags(self.c, self.node_name, self.group_name, tags_data, request_name)