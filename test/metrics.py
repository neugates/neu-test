import logging

from locust import HttpUser, task, between
from prometheus_client.parser import text_string_to_metric_families

import common.api as api
import common.config as config


class MetricsUser(HttpUser):
    wait_time = between(30, 30)

    def on_start(self):
        self.c = api.NeuronAPI(self.client)
        self.last_memory = 0
        self.init_memory = 0

    def get_value(self, key, text):
        for family in text_string_to_metric_families(text):
            for sample in family.samples:
                if sample.name == key:
                    return sample.value
        raise ValueError("key not found")

    @task
    def check_coredump(self):
        with self.c.get_metrics() as response:
            response.request_meta['name'] = "core dump"
            try:
                value = self.get_value('core_dumped', response.text)
            except ValueError as e:
                response.failure('no core dump' + str(e))
            else:
                if value == 0.0:
                    response.success()
                else:
                    response.failure('coredump: ' + str(value))

    @task
    def check_memory(self):
        with self.c.get_metrics() as response:
            response.request_meta['name'] = "memory check"
            try:
                value = self.get_value('mem_used_bytes', response.text)
            except ValueError as e:
                response.failure('no mem used bytes' + str(e))
            else:
                current = value / 1024/1024
                if self.init_memory == 0:
                    self.init_memory = current
                if self.last_memory > 0 and current - self.last_memory > 10:
                    logging.warning('memory is growing, current: ' +
                                    str(current) + ' last: ' + str(self.last_memory))
                    response.failure('memory is growing, current: ' +
                                     str(current) + ' last: ' + str(self.last_memory))
                else:
                    self.last_memory = current
                    response.success()
                    logging.warning('current memory: ' +
                                    str(current) + ', init memory: ' + str(self.init_memory))
