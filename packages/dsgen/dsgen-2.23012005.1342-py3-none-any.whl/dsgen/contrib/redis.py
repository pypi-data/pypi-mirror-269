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
# dsgen.contrib.redis

import base64
from datetime import timedelta
from uuid import uuid4

from dsgen.runtime import ObjectLoader
from .base import BackingStore


class RedisStore(BackingStore):
    CLASS_CONNECTION = 'redis.Redis'

    def generate_unique_key(self, obj):
        return str(uuid4())

    @property
    def connectionParams(self):
        d = {
            'host': 'localhost',
        }
        return d

    def getRedisConnection(self):
        kls = ObjectLoader().loadByName(self.CLASS_CONNECTION)
        return kls(**self.connectionParams)

    @property
    def ttlOption(self):
        d = {
            'minutes': 5,
        }
        return d

    def getTimeLimit(self, obj):  # pylint: disable=W0613
        return timedelta(**self.ttlOption)

    def toStream(self, obj):
        return base64.b64encode(obj)

    def toInternalRepresentation(self, data):
        return base64.b64decode(data)

    def doDeposite(self, obj):
        val = None

        db = self.getRedisConnection()
        try:
            key = self.generate_unique_key(obj)
            _ret = db.setex(
                key,
                self.getTimeLimit(obj),
                self.toStream(obj)
            )
            if _ret:
                val = key
        except Exception as _ex:  # pylint: disable=W0718
            self.onDepositeError(_ex)
        finally:
            del db
        return val

    def onDepositeError(self, exc=None):  # pylint: disable=W0613
        return

    def doRetrieve(self, key):
        val = None

        db = self.getRedisConnection()
        try:
            val = self.toInternalRepresentation(
                db.get(key)
            )
        except Exception as _ex:  # pylint: disable=W0718
            self.onRetrieveError(_ex)
        finally:
            del db
        return val

    def onRetrieveError(self, exc=None):  # pylint: disable=W0613
        return
