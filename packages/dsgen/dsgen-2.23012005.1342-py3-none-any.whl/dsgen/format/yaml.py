# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2019, 2020, 2021 Xingeng Chen
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
# dsgen.format.yaml

import yaml

from dsgen.file import FileReader, ReaderError


class YAMLReader(FileReader):
    '''
    I read a file and parse its content as YAML stream
    '''

    MSG_READ_ERROR = 'Unable to load YAML file'

    def doRead(self):
        rval = None
        try:
            with open(self._path, 'r') as _f:
                cache = [ x for x in yaml.safe_load_all(_f) if x ]
                rval = dict()
                [ rval.update(x) for x in cache ]
        except Exception as ex:
            raise ReaderError(self.MSG_READ_ERROR, path=self._path) from ex
        return rval
