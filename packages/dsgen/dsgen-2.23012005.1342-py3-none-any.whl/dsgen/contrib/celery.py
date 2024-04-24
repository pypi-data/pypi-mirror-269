# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2019, 2020, 2021 Xingeng Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# dsgen.contrib.celery

from dsgen.runtime import ObjectLoader
from dsgen.task import TaskDispatcher, TaskSchedule


class CeleryTaskSchedule(TaskSchedule):

    CLASS_CRONTAB = 'celery.schedules.crontab'
    CLASS_T_DELTA = 'datetime.timedelta'

    def _load_preset(self):
        self._loader = ObjectLoader()
        self._crontab_cls = self._loader.loadByName(self.CLASS_CRONTAB)
        self._t_delta_cls = self._loader.loadByName(self.CLASS_T_DELTA)

        return super()._load_preset()


class CeleryHelper(TaskDispatcher):
    '''
    I deal with celery task routing
    '''

    CLASS_MESSAGE_EXCHANGE = 'kombu.Exchange'
    CLASS_MESSAGE_QUEUE    = 'dsgen.contrib.amqp.Queue'

    def __init__(self, parent):
        '''
        :param parent: config provider (object)
        '''

        super().__init__()
        self.parent = parent
        self._load_preset()

    def _load_preset(self):
        self._loader = ObjectLoader()

        self._exchange_cls = self._loader.loadByName(self.CLASS_MESSAGE_EXCHANGE)
        self._queue_cls = self._loader.loadByName(self.CLASS_MESSAGE_QUEUE)
        return self

    def convert_queue_definition(self, data):
        '''
        construct Celery queue definition

        ```json
        {
            "name": "demo",
            "exchange": "demo",
            "exchange.type": "direct",
            "routing_key": "task"
        }
        ```

        :param data: plain values from JSON (dict)

        :return: conversion result (dict)
        '''

        _exchange_cls = self.get_exchange_cast()
        _queue_cls = self.get_queue_cast()

        exch = _exchange_cls(
            data.get(
                'exchange',
                data['name']
            ),
            type=data.get(
                'exchange.type',
                'fanout'
            ),
        )
        queue = _queue_cls(
            data['name'],
            exch,
            routing_key=data['routing_key'],
            selection=data.get('selection', None),
        )
        return queue


class DSCeleryConfig(CeleryHelper):
    '''
    helper class for Celery task schedule and queue definition
    '''

    def _load_preset(self):
        super()._load_preset()

        self._schedule = CeleryTaskSchedule()
        return self

    def create_schedule(self, data):
        '''
        construct Celery schedule objects

        ```json
        {
            "task-every-30-minutes": {
                "task": "app.tasks.a_simple_task",
                "schedule": "minutes=30"
            },
            "task-at-specific-hours": {
                "task": "app.tasks.another_task",
                "schedule": {
                    "minute": "3",
                    "hour": "0,1,2,6,7,8,9,10,11"
                }
            }
        }
        ```

        :param data: plain values from JSON (dict)
        :return: conversion result (dict)
        '''
        return self._schedule.dictToSchedule(data)
