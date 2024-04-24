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
# dsgen.file.exception

class ReaderError(RuntimeError):
    '''
    Signal for reader errors
    '''

    def __init__(self, msg, path):
        super().__init__(msg)
        self.path = path

    def __str__(self):
        return f"{super().__str__()}: {self.path}"
