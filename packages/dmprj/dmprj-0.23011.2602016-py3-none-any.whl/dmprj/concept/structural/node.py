# -*- python -*-
#
# Copyright 2021, 2022, 2023 Xingeng Chen (Chen Studio)
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
# dmprj.concept.structural.node


class Node():
    '''
    base class
    '''


class ExtensibleNode(Node):
    '''
    a composition of multiple nodes
    '''

    @property
    def children(self):
        raise NotImplementedError()


class TextualNode(Node):
    '''
    node with textual representation
    '''

    FMT_INORDER_PLUS_FIX = '{outer_a}{prefix}{name}{inner_a}{children}{inner_b}{suffix}{outer_b}'

    def toString(self):
        raise NotImplementedError()
