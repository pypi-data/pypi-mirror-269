# -*- python -*-
#
# Copyright 2021, 2022, 2023 Xingeng Chen (Chen Studio)
# Copyright 2018, 2019, 2020, 2021 Liang Chen (Chen Studio)
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
#
# dmprj.engineering.versioncontrol.actions


from .base import VersionControlAction


class APPLY(VersionControlAction):
    '''
    FROM pool TO wspace
    '''

class BLEND(VersionControlAction):
    '''
    FROM image TO pool
    '''

class CAPTURE(VersionControlAction):
    '''
    FROM wspace TO pool
    '''

class DISTILL(VersionControlAction):
    '''
    FROM pool TO image
    '''

class FLUX(VersionControlAction):
    '''
    WITHIN pool
    '''
