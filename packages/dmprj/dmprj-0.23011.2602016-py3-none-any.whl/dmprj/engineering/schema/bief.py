# -*- python -*-
#
# Copyright 2021, 2022, 2023 Xingeng Chen, Cecelia Chen (Chen Studio)
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
# dmprj.engineering.schema.bief
#
# Backend Independent Exchange Format

from dmprj.concept.structural.entity import AttributeWithValue, MultiValueAttribute

from .base import Format


class BIEFField(AttributeWithValue):
    '''
    single value field
    '''

    FMT_STR = '{name}:{flag}{spacer}{value}'
    SPACER = ' '

    def __str__(self):
        val = self.FMT_STR.format(
            flag=self.get_value_type_flag(),
            spacer=self.SPACER,
            #
            name=self.name,
            value=self.value,
        )
        return val

    def get_value_type_flag(self):
        flag = ''
        if getattr(self, 'encoded_stream', False):
            flag = ':'
        return flag

    @property
    def name(self):
        return None

    @property
    def value(self):
        return None


class BIEFMVField(MultiValueAttribute):
    '''
    multi-value field
    '''

    CHILD = BIEFField

    @property
    def name(self):
        return None

    @property
    def value(self):
        return None


class BIEFEntity(object):
    '''
    a representation of an entity
    '''

    def loadFromData(self, data):
        return self

    def __repr__(self):
        return None

    def __str__(self):
        cache = list()
        # first line;
        cache.append(
            str(self.get_dn())
        )
        for af in self.get_fields():
            cache.append(
                str(af)
            )
        return '\n'.join(cache)


class BIEF(Format):
    '''
    BIEF -- backend independent exchange format
    '''

    def to_presentation(self, instance):
        ret = ''
        return ret

    def to_python(self, data):
        entity = BIEFEntity()
        return entity.loadFromData(data)

    def startDocument(self):
        # add header components to internal cache;
        return self

    def endDocument(self):
        # add footer components to internal cache;
        return self
