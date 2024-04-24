# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Xingeng Chen
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
# dsgen.schema.base

from dmprj.concept.behavioral import Selector


class GrossCheck(Selector):
    '''
    I do gross check based on critera given by my parent
    '''

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self.minimum_level = 1

    def accept(self, item):
        actual_count = item.count(self._parent.primary_delimiter)
        if actual_count >= self.minimum_level:
            return True
        return None

    def reject(self, item):
        if self._parent.primary_delimiter not in item:
            return False
        return None


class Delimiter:  # pylint: disable=E1101

    SPACE = ' '
    SEMICOLON = ';'

    COLON = ':'
    EQUAL = '='
    CARET = '^'
    PIPE = '|'
    TILDE = '~'
    PERCENT = '%'
    AMPERSAND = '&'
    ASTERISK = '*'

    FORWARD_SLASH = '/'
    BACK_SLASH = '\\'

    def get_tokens(self, x):
        '''
        :param x: (string)
        '''
        return x.split(self.primary_delimiter)

    def split_key_value(self, x):
        '''
        :param x: (string)
        '''
        return x.split(self.argument_delimiter, 1)


class SpaceDelimited(Delimiter):
    '''
    SPACE as the primary delimiter
    '''

    def __init__(self):
        super().__init__()
        self.check_helper = GrossCheck(self)

    @property
    def primary_delimiter(self):
        return self.SPACE

    def accept(self, item):
        return self.check_helper.accept(item)


class SemicolonDelimited(Delimiter):
    '''
    SEMICOLON as the primary delimiter
    '''

    def __init__(self):
        super().__init__()
        self.check_helper = GrossCheck(self)

    @property
    def primary_delimiter(self):
        return self.SEMICOLON

    def accept(self, item):
        return self.check_helper.accept(item)
