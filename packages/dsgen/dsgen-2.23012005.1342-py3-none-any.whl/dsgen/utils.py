# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Xingeng Chen
# Copyright 2016, 2017, 2018 Liang Chen
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
# dsgen.utils

from .base import ProjectSettingBase, SettingBase
from .message import MSG_FORMAT_ERROR_LOADING_JSON
from .runtime import ObjectLoader


class DSGenerator(ProjectSettingBase):
    '''
    I should be subclassed for Django project setting, and my
    instance methods should override module-level reference:
    `__dir__` => `get_config_field_list`
    `__getattr__` => get_config_value`
    '''

    def __init__(self, json_path=None, reader='dsgen.format.json.JSONReader'):
        '''
        :param json_path: (string)
        :param reader: (string)
        '''
        super().__init__()
        self._loader = ObjectLoader()

        if json_path is not None:
            try:
                reader_cls = self._loader.loadByName(reader)
                self.site_config.update(
                    reader_cls(json_path).doRead()
                )
            except Exception:
                from django.core.exceptions import ImproperlyConfigured  # noqa
                msg = MSG_FORMAT_ERROR_LOADING_JSON.format(fp=json_path)
                bad_config = ImproperlyConfigured(msg)
                raise bad_config  # pylint: disable=W0707

            self.site_json_path = json_path
        self.collect_apps()


class DSetting(SettingBase):
    '''
    I should be subclassed for Django app setting

    subclass MUST declare the following attributes:
    - `DEFAULT` (dict)
    - `SETTING_NAME` (string)
    '''

    def _ctor_load(self):
        self._default = self.DEFAULT
        self._cache_key = set()
        from django.conf import settings as _ds_conf  # noqa
        self._ds_conf = _ds_conf
        return super()._ctor_load()
