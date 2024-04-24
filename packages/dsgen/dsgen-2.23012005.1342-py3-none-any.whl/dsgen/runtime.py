# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
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
# dsgen.runtime

from dmprj.engineering.boot import ObjectLoader as _base_loader


class ObjectLoader(_base_loader):
    '''
    I deal with target object loading at runtime
    '''

    def loadByName(self, name):
        '''
        :param name: (string)
        '''

        _obj = None
        from django.utils.module_loading import import_string  # noqa
        try:
            _obj = import_string(name)
        except:  # pylint: disable=W0702
            if getattr(self, 'use_exc', False):
                raise
            self.onLoadError()
        return _obj

    def onLoadError(self):
        return
