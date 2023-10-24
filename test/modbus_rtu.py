import logging

from locust import HttpUser, task, between

import common.api as api
import common.config as config
import common.modbus as modbus


class ModbusRTUSensor(HttpUser):
    wait_time = between(0.1, 2)

    # temperature/humidity sensor

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task
    def read_temperature(self):
        pass

    @task
    def read_humidity(self):
        pass
