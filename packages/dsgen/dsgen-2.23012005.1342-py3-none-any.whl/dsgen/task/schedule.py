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
# dsgen.task.schedule


class TaskSchedule:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_preset()

    def _load_preset(self):
        return self

    def dictToSchedule(self, data):
        val = dict()
        val.update(data)
        for task, task_conf in val.items():
            raw_val = task_conf['schedule']
            try:
                val[ task ]['schedule'] = self.toIncrementalSchedule(raw_val)
            except AttributeError:
                val[ task ]['schedule'] = self.toFixedSchedule(raw_val)
            except ValueError:
                self.onInvalidSchedule()

        return val

    def toIncrementalSchedule(self, data):
        '''
        :param data: (string)

        :throw AttributeError: if input is incompatible datatype or invalid
        '''

        tokens = data.split('=', 1)
        _param = {
            tokens[0]: int(tokens[1]),
        }
        return self._t_delta_cls(**_param)

    def toFixedSchedule(self, data):
        '''
        :param data: (dict)
        '''

        return self._crontab_cls(**data)

    def onInvalidSchedule(self):
        # currently we just drop the incorrectly defined items;
        return
