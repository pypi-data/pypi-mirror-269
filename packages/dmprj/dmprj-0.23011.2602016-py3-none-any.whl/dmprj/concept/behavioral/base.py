# -*- python -*-
#
# Copyright 2021, 2022, 2023 Xingeng Chen (Chen Studio)
# Copyright 2016, 2017, 2018, 2019, 2020, 2021 Liang Chen (Chen Studio)
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
# dmprj.concept.behavioral.base


from dmprj.base.messages import MSG_NOT_IMPLEMENTED


class Action(object):
    '''
    I carry out operations
    '''

    def do(self):
        '''
        NOTE: template method
        '''
        self.prologue()
        self.main_play()
        self.epilogue()
        return None

    def prologue(self):
        return NotImplementedError(MSG_NOT_IMPLEMENTED)

    def main_play(self):
        return NotImplementedError(MSG_NOT_IMPLEMENTED)

    def epilogue(self):
        return NotImplementedError(MSG_NOT_IMPLEMENTED)


class Selector:  # pylint: disable=W0613
    '''
    I define basic methods.
    '''

    def accept(self, item):
        return None

    def reject(self, item):
        return None
