# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen (Chen Studio)
# Copyright 2019, 2020, 2021 Xingeng Chen (Chen Studio)
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
# dsgen.contrib.amqp

from dmprj.concept.behavioral import Selector
from kombu import Queue as _ampq_queue

from dsgen.schema.parser import NamespaceParameterParser


class TaskNameFilter:
    '''
    delegatee for accepting task by name

    ```python
    TaskNameFilter(
        NamespaceParameterParser().do(
            "TaskNameFilter;target:item;op:startswith;value:dumb-text"
        )
    )
    ```
    '''

    LABEL_NAMESPACE = 'namespace'

    LABEL_TARGET    = 'target'
    LABEL_OPERATION = 'op'
    LABEL_VALUE     = 'value'

    def __init__(self, logic):
        '''
        :param logic: (dict)
        '''
        self._data = logic
        self._check()

    def _check(self):
        assert self._data[ self.LABEL_NAMESPACE ] == self.__class__.__name__, 'invalid input'
        return self

    def _get_subject_handler(self, subj):
        target_attr = self._data[ self.LABEL_OPERATION ]

        _fh = getattr(
            subj,
            target_attr
        )
        return _fh

    def onError(self):
        return

    def __call__(self, x):
        val = None

        try:
            _func = self._get_subject_handler(x)
            val = _func(self._data[ self.LABEL_VALUE ])
        except:  # pylint: disable=W0702
            self.onError()
        return val


class QueueGateKeeper(Selector):
    '''
    I am in charge of picking tasks based on loaded rules;
    when no rules are assigned to me, I will accept everyone.
    '''

    def __init__(self):
        super().__init__()
        self._selection_rules = list()

    def load(self, ruleset=None):
        '''
        :param ruleset: (iterable)
        '''

        try:
            for item in ruleset:
                try:
                    filter = TaskNameFilter(
                        NamespaceParameterParser().do(item)
                    )
                    self._selection_rules.append(
                        filter
                    )
                except:  # pylint: disable=W0702
                    self.onFilterCreationError()
        except:  # pylint: disable=W0702
            self.onLoadError()
        return self

    def onLoadError(self):
        return

    def onFilterCreationError(self):
        return

    def accept(self, item):
        '''
        :return: (bool)
        '''

        flag = False

        if self._selection_rules:
            for each in self._selection_rules:
                try:
                    assert each(item), 'skip'
                    flag = True
                    break
                except:  # pylint: disable=W0702
                    self.onRuleInvocationError()
        else:
            flag = True
        return flag

    def onRuleInvocationError(self):
        return


class Queue(_ampq_queue):
    '''
    I add additional methods on top of `kombu.Queue`.

    A list of strings may be passed to Ctor for optional argument `selection`,
    each string should be in format of "item;op:startswith;value:dumb-text"
    '''

    CONTRIB_ATTRS = (
        ('selection', None),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__preload_selection_rule()

    def __preload_selection_rule(self):
        self._gatekeeper = QueueGateKeeper()
        self._gatekeeper.load(
            getattr(
                self,
                'selection',
                list()
            )
        )
        return self

    @property
    def attrs(self) -> tuple:
        base = list(super().attrs)
        contrib = list(self.CONTRIB_ATTRS)
        return tuple(base + contrib)

    def accept(self, item):
        '''
        :param item: (string)

        :return: whether the queue should accept the given task (bool)
        '''

        return self._gatekeeper.accept(item)
