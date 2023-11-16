import random
import string
import logging

from locust import HttpUser

import common.config as config


def random_string(length=8):
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))


def random_driver_name():
    return 'driver_' + random_string(8)


def random_group_name():
    return 'group_' + random_string(8)


def random_tag_name():
    return 'tag_' + random_string(8)


def random_app_name():
    return 'app_' + random_string(8)


class NeuronAPI():
    def __init__(self, client):
        self.client = client

    def get_metrics(self):
        return self.client.get(url="/api/v2/metrics", catch_response=True)

    def add_node(self, node, plugin):
        return self.client.post(url="/api/v2/node", json={"name": node, "plugin": plugin}, headers={
            "Authorization": config.default_jwt}, catch_response=True)

    def del_node(self, node):
        return self.client.delete(url="/api/v2/node", json={"name": node}, headers={"Authorization": config.default_jwt}, catch_response=True)

    def start_node(self, node):
        return self.client.post(url="/api/v2/node/ctl", json={"node": node, "cmd": 0}, headers={"Authorization": config.default_jwt}, catch_response=True)

    def stop_node(self, node):
        return self.client.post(url="/api/v2/node/ctl", json={"node": node, "cmd": 1}, headers={"Authorization": config.default_jwt}, catch_response=True)

    def node_setting(self, node, json):
        return self.client.post(url="/api/v2/node/setting", json={"node": node, "params": json}, headers={
            "Authorization": config.default_jwt}, catch_response=True)

    def add_group(self, node, group, interval=100):
        return self.client.post(url="/api/v2/group", json={"node": node, "group": group, "interval": interval}, headers={
            "Authorization": config.default_jwt}, catch_response=True)

    def add_tags(self, node, group, tags):
        return self.client.post(url="/api/v2/tags", json={"node": node, "group": group, "tags": tags}, headers={
            "Authorization": config.default_jwt}, catch_response=True)

    def read_tags(self, node, group, sync=False):
        return self.client.post(url="/api/v2/read", json={"node": node, "group": group, "sync": sync}, headers={
            "Authorization": config.default_jwt}, catch_response=True)

    def read_and_update_tags(self, node, group, map_tags):
        with self.client.post(url="/api/v2/read", json={"node": node, "group": group, "sync": False}, headers={
                "Authorization": config.default_jwt}, catch_response=True) as response:
            if response.status_code == 200:
                tags = response.json()['tags']
                for tag in tags:
                    if tag['name'] in map_tags:
                        if tag.get('value') is not None:
                            map_tags[tag['name']]['value'] = tag['value']
                        elif tag.get('error') is not None:
                            map_tags[tag['name']]['value'] = tag['error']

    def write_tag(self, node, group, tag, value):
        return self.client.post(url="/api/v2/write", json={"node": node, "group": group, "tag": tag,
                                                           "value": value}, headers={"Authorization": config.default_jwt}, catch_response=True)

    def write_tags(self, node, group, tag_values):
        return self.client.post(url="/api/v2/writes", json={"node": node, "group": group, "tags": tag_values},
                                headers={"Authorization": config.default_jwt}, catch_response=True)

    def modbus_tcp_node_setting(self, node, host, port, connection_mode=0, transport_mode=0, interval=0, timeout=3000):
        return self.node_setting(node, json={"connection_mode": connection_mode, "transport_mode": transport_mode, "interval": interval,
                                             "host": host, "port": port, "timeout": timeout})

    def s7comm_node_setting(self, node, host, port, local_tsap=0, remote_tsap=0, pdu_size=960, connection_type=1, module=0, rack=0, slot=1):
        return self.node_setting(node, json={"host": host, "port": port, "local_tsap": local_tsap, "remote_tsap": remote_tsap,
                                             "pdu_size": pdu_size, "connection_type": connection_type, "module": module, "rack": rack, "slot": slot})
