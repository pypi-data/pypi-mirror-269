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
# dsgen.task.dispatch

from dmprj.engineering.chore import Dispatcher

from dsgen.message import MSG_VIRTUAL_METHOD_CALLED


class TaskDispatcher(Dispatcher):

    def route_for_task(self, task, *args, **kwargs):  # pylint: disable=W0613
        '''
        :param task: (object)
        '''
        return NotImplementedError(MSG_VIRTUAL_METHOD_CALLED)

    def get_exchange_cast(self):
        return self._exchange_cls

    def get_queue_cast(self):
        return self._queue_cls
