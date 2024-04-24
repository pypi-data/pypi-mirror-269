# -*- python -*-
#
# Copyright 2020, 2021, 2022, 2023 Xingeng Chen (Chen Studio)
# Copyright 2015, 2016, 2017, 2018, 2019 Liang Chen (Chen Studio)
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
# dmprj.engineering.boot.loader

import importlib
import sys


class ObjectLoader:
    '''
    I can load other object dynamically
    '''

    def parseName(self, name):
        path, label = name.rsplit('.', 1)
        return {'path':path, 'label':label}

    def importModule(self, mod):
        return importlib.import_module(mod)

    def loadByName(self, name):
        _obj = None
        try:
            ns = self.parseName(name)
            mod = self.importModule(ns['path'])
            _obj = getattr(mod, ns['label'])
        except:  # pylint: disable=W0702,W0707
            if getattr(self, 'use_exc', False):
                _msg = f'fail to import {name}'
                raise ImportError(_msg)
            self.onLoadError()
        return _obj


class CachedObjectLoader(ObjectLoader):
    '''
    I use system cache to speed up
    '''

    def checkSysCache(self, ns):
        try:
            mod = sys.modules[ ns['path'] ]
            status = getattr(
                mod.__spec__,
                '_initializing'
            )
            assert status is False
            ret = mod
        except:  # pylint: disable=W0702
            ret = None
        return ret

    def loadByName(self, name):
        _obj = None
        try:
            ns = self.parseName(name)
            mod = self.checkSysCache(ns)
            if mod is None:
                mod = self.importModule(ns['path'])
            _obj = getattr(mod, ns['label'])
        except:  # pylint: disable=W0702,W0707
            if getattr(self, 'use_exc', False):
                _msg = f'fail to import {name}'
                raise ImportError(_msg)
            self.onLoadError()
        return _obj
