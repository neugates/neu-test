import logging
import os

from locust import HttpUser, task, between

import common.api as api
import common.config as config
from common.fins import (fins_gen_tag, fins_node_setting)
import common.tag as ctag


class FinsUdpRandom(HttpUser):
    wait_time = between(0.1, 2)

    def on_start(self):
        self.node_name = "fins_udp"
        self.group_name = "group_1"
        self.tags = []
        self.tags += ctag.random_tag(fins_gen_tag, 100, 'CIO')
        self.tags += ctag.random_tag(fins_gen_tag, 100, 'D')

        self.map_tags = {}
        for tag in self.tags:
            self.map_tags[tag['name']] = tag

        self.c = api.NeuronAPI(self.client)
        self.c.del_node(self.node_name)
        self.c.add_node(self.node_name, config.PLUGIN_FINS_UDP)
        self.c.add_group(self.node_name, self.group_name, 100)
        fins_node_setting(self.c, self.node_name, '192.168.10.107', 9600, 6)
        self.c.add_tags(self.node_name, self.group_name, self.tags)

    def on_stop(self):
        self.c.stop_node(self.node_name)

    @task(10)
    def read_tags(self):
        request_name = "fins udp random read tags"
        ctag.read_and_check(self.c,
                            request_name, self.node_name, self.group_name)

    @task(1)
    def write_tag(self):
        request_name = "fins udp random write tag"
        ctag.write_and_check(self.c, self.tags, self.map_tags,
                             request_name, self.node_name, self.group_name)

    @task(1)
    def write_tags(self):
        pass
