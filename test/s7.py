import logging
import random
import time
import os

from locust import HttpUser, task, between

import common.api as api
import common.config as config
import common.tag as ctag


def gen_tag(area, db_number, plc_mode):
    if plc_mode == '200':
        address = random.randint(0, 1024)
    else:
        address = random.randint(0, 260)

    if area == 'I' or area == 'O' or area == 'C' or area == 'T':
        address = random.randint(0, 30)
    elif area == 'F':
        address = random.randint(0, 20)
    attribute = config.NEU_TAG_ATTRIBUTE_RW
    type = config.NEU_TYPE_INT16

    if area == 'I':
        type = ctag.random_type(
            [config.NEU_TYPE_BIT, config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16])
        address = 'I' + str(address)
        attribute = config.NEU_TAG_ATTRIBUTE_READ
    elif area == 'O':
        type = ctag.random_type(
            [config.NEU_TYPE_BIT, config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16])
        address = 'O' + str(address)
        attribute = config.NEU_TAG_ATTRIBUTE_READ
    elif area == 'C':
        type = ctag.random_type(
            [config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16])
        address = 'C' + str(address)
    elif area == 'T':
        type = ctag.random_type(
            [config.NEU_TYPE_INT32, config.NEU_TYPE_UINT32])
        address = 'T' + str(address)
    elif area == 'DB':
        type = ctag.random_type([config.NEU_TYPE_INT8, config.NEU_TYPE_UINT8,
                                config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16,
                                config.NEU_TYPE_INT32, config.NEU_TYPE_UINT32,
                                config.NEU_TYPE_FLOAT, config.NEU_TYPE_DOUBLE,
                                config.NEU_TYPE_BIT, config.NEU_TYPE_STRING])
        if plc_mode == '1200' and address > 150:
            type = config.NEU_TYPE_INT32
        address = 'DB' + str(db_number) + '.DBW' + str(address)
    elif area == 'F':
        type = ctag.random_type([config.NEU_TYPE_INT8, config.NEU_TYPE_UINT8,
                                config.NEU_TYPE_INT16, config.NEU_TYPE_UINT16,
                                config.NEU_TYPE_INT32, config.NEU_TYPE_UINT32,
                                config.NEU_TYPE_FLOAT, config.NEU_TYPE_DOUBLE,
                                config.NEU_TYPE_BIT])
        address = 'F' + str(address)

    n_byte = 0
    if type == config.NEU_TYPE_BIT:
        bit = random.randint(0, 7)
        address = address + '.' + str(bit)
    elif type == config.NEU_TYPE_STRING:
        length = random.randrange(10, 128, 2)
        address = address + '.' + str(length)
        n_byte = length

    return address, type, attribute, n_byte


class S7200SmartRandom(HttpUser):
    wait_time = between(0.1, 2)

    def on_start(self):
        self.node_name = "s7200_smart_random"
        self.group_name = "group_1"
        self.tags = []
        self.tags += ctag.random_tag(gen_tag, 100, 'I', 1, '200')
        self.tags += ctag.random_tag(gen_tag, 100, 'O', 1, '200')
        # self.tags += tag.random_tag(gen_tag, 100, 'C', 1, '200')
        # self.tags += tag.random_tag(gen_tag, 100, 'T', 1, '200')
        self.tags += ctag.random_tag(gen_tag, 100, 'F', 1, '200')
        self.tags += ctag.random_tag(gen_tag, 100, 'DB', 1, '200')

        self.map_tags = {}
        for tag in self.tags:
            self.map_tags[tag['name']] = tag

        self.c = api.NeuronAPI(self.client)
        self.c.del_node(self.node_name)
        self.c.add_node(self.node_name, config.PLUGIN_S7COMM)
        self.c.add_group(self.node_name, self.group_name, 100)
        arch = os.environ.get('ARCH')
        if arch == 'amm32':
            self.c.s7comm_node_setting(
                self.node_name, '192.168.10.106', 102, connection_type=3)
        elif arch == 'arm64':
            self.c.s7comm_node_setting(
                self.node_name, '192.168.10.106', 102, connection_type=2)
        else:
            self.c.s7comm_node_setting(self.node_name, '192.168.10.106', 102)
        self.c.add_tags(self.node_name, self.group_name, self.tags)

    def on_stop(self):
        self.c.stop_node(self.node_name)

    @task(10)
    def read_tags(self):
        request_name = "s7 200 random read tags"
        ctag.read_and_check(self.c,
                            request_name, self.node_name, self.group_name)

    @task(1)
    def write_tag(self):
        request_name = "s7 200 random write tag"
        ctag.write_and_check(self.c, self.tags, self.map_tags,
                             request_name, self.node_name, self.group_name)

    @task(1)
    def write_tags(self):
        pass


# class S7200SmartFixed(HttpUser):
    # wait_time = between(0.1, 2)

    # def on_start(self):
        # pass

    # def on_stop(self):
        # pass

    # @task(10)
    # def read_tags(self):
        # pass

    # @task(1)
    # def write_tag(self):
        # pass

    # @task(1)
    # def write_tags(self):
        # pass


class S71200Random(HttpUser):
    wait_time = between(0.1, 2)

    def on_start(self):
        self.node_name = "s71200_random"
        self.group_name = "group_1"
        self.tags = []
        self.tags += ctag.random_tag(gen_tag, 100, 'I', 1, '1200')
        self.tags += ctag.random_tag(gen_tag, 100, 'O', 1, '1200')
        # self.tags += tag.random_tag(gen_tag, 100, 'C', 1 ,'1200')
        # self.tags += tag.random_tag(gen_tag, 100, 'T', 1, '1200')
        self.tags += ctag.random_tag(gen_tag, 100, 'F', 1, '1200')
        self.tags += ctag.random_tag(gen_tag, 100, 'DB', 2, '1200')

        self.map_tags = {}
        for tag in self.tags:
            self.map_tags[tag['name']] = tag

        self.c = api.NeuronAPI(self.client)
        self.c.del_node(self.node_name)
        self.c.add_node(self.node_name, config.PLUGIN_S7COMM)
        self.c.add_group(self.node_name, self.group_name, 100)
        self.c.s7comm_node_setting(self.node_name, '192.168.10.101', 102)
        self.c.add_tags(self.node_name, self.group_name, self.tags)
        pass

    def on_stop(self):
        self.c.stop_node(self.node_name)

    @task(10)
    def read_tags(self):
        request_name = "s7 1200 random read tags"
        ctag.read_and_check(self.c,
                            request_name, self.node_name, self.group_name)

    @task(1)
    def write_tag(self):
        request_name = "s7 1200 random write tag"
        ctag.write_and_check(self.c, self.tags, self.map_tags,
                             request_name, self.node_name, self.group_name)

    @task(1)
    def write_tags(self):
        pass


# class S71200Fixed(HttpUser):
    # wait_time = between(0.1, 2)

    # def on_start(self):
        # pass

    # def on_stop(self):
        # pass

    # @task(10)
    # def read_tags(self):
        # pass

    # @task(1)
    # def write_tag(self):
        # pass

    # @task(1)
    # def write_tags(self):
        # pass
