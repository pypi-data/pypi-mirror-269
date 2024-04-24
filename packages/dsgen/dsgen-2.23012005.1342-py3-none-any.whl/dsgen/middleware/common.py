# -*- python -*-
#
# Copyright 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 Xingeng Chen (Chen Studio)
# Copyright 2015, 2016, 2017 Liang Chen (Chen Studio)
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
# dsgen.middleware.common

from django.core.exceptions import DisallowedHost
from django.http import HttpResponseForbidden
from django.middleware.common import CommonMiddleware as _dj_common_mw


class CommonMiddleware(_dj_common_mw):

    response_class = HttpResponseForbidden

    def process_request(self, request):
        try:
            return super().process_request(request)
        except DisallowedHost:
            return self.response_class('Forbidden')
        except:
            raise
