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
# dsgen.base

from .message import MSG_VIRTUAL_METHOD_CALLED


class DSBase:  # pylint: disable=W0201,E1101
    '''
    I define basic methods.

    subclass MUST declare the following attributes:
    - `default_app_list` (list of string)
    '''

    def collect_apps(self, extra=None):  # pylint: disable=W0613
        self.INSTALLED_APPS = list()
        self.INSTALLED_APPS.extend(self.default_app_list)
        return self

    def get_config_field_list(self):
        raise NotImplementedError(MSG_VIRTUAL_METHOD_CALLED)

    def get_config_value(self, name):
        '''
        :param name: (string)
        '''
        raise NotImplementedError(MSG_VIRTUAL_METHOD_CALLED)


class ProjectSettingBase(DSBase):

    def __init__(self):
        super().__init__()
        self.site_config = dict()

    def get_config_field_list(self):
        '''
        :return: (list of string)
        '''

        attr_fields = [ attr for attr in dir(self) if attr.isupper() ]
        dict_fields = list(self.site_config.keys())
        dict_extra_fields = [ each for each in dict_fields if each not in attr_fields ]
        # rvalue;
        all_fields = list()
        all_fields.extend(attr_fields)
        all_fields.extend(dict_extra_fields)
        return all_fields

    def get_config_value(self, name):
        '''
        :param name: (string)
        '''

        if name.startswith('_'):
            value = globals().get(name)
        else:
            value = getattr(
                self,
                name,
                self.site_config.get(name)
            )
        return value


class SettingBase:  # pylint: disable=R1711
    '''
    I define basic methods.

    subclass MUST declare the following attributes:
    - `SETTING_NAME` (string)

    subclass MAY override the following methods:
    - `get_passthrough_fields` (list/tuple)
    '''

    def __init__(self):
        super().__init__()
        self._ctor_load()

    def _ctor_load(self):
        return self

    def get_passthrough_fields(self):
        '''
        This provides a list of attribute names which should be delegated to project setting.

        :return: (list/tuple of string)
        '''

        pass_through_list = list()
        return pass_through_list

    def __getattr__(self, attr):
        '''
        :param attr: (string)
        '''

        if attr in self.get_passthrough_fields():
            return getattr(self._ds_conf, attr)

        try:
            val = self.site_conf[attr]
        except KeyError:
            try:
                val = self._default[attr]
            except KeyError:
                _msg = f"Invalid setting: '{attr}'"
                raise AttributeError(_msg)  # pylint: disable=W0707

        self._cache_key.add(attr)
        setattr(self, attr, val)
        return val

    def signal_handler_setting_changed(self, *args, **kwargs):  # pylint: disable=W0613
        '''
        stub handler for `django.test.signals.setting_changed`
        '''

        if kwargs['setting'] == self.SETTING_NAME:
            self.reload()
        return None

    def reload(self):
        '''
        flush cached values
        '''

        for item in self._cache_key:
            delattr(self, item)
        self._cache_key.clear()
        if hasattr(self, '_site'):
            delattr(self, '_site')
        return None

    @property
    def site_conf(self):
        if '_site' not in self.__dict__:
            _conf = getattr(
                self._ds_conf,
                self.SETTING_NAME,
                dict()
            )
            setattr(
                self,
                '_site',
                _conf
            )
        return self.__dict__['_site']
