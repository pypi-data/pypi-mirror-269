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
# dsgen.contrib.base

from dsgen.message import MSG_VIRTUAL_METHOD_CALLED


class BackingStore:  # pylint: disable=E1101,W0613

    def generate_unique_key(self, obj):
        raise NotImplementedError(MSG_VIRTUAL_METHOD_CALLED)

    def toStream(self, obj):
        return None

    def toInternalRepresentation(self, data):
        return None

    def deposite(self, obj):
        return self.doDeposite(obj)

    def retrieve(self, key):
        return self.doRetrieve(key)
