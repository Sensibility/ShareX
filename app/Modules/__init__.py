import json
import os

from .base_module import Module


class ModuleFactory(Module):
    modules = {}
    root = ""

    def Bootstrap(self):
        dir = os.getcwd() + "/private/config/"
        try:
            f = open(dir + "conf.json", 'r')
        # For the build agent/testing
        except:
            f = open(dir + "conf.orig.json", 'r')

        config = json.loads(str.join("", f.readlines()))
        mods = config.get('Modules')

        if config.get('Root'):
            self.root = config.get('Root')

        for key in mods.keys():
            mod = mods.get(key)
            self.modules[key] = self.modules[key](mod, self.root)

        f.close()

    def Register(self, classRef):
        self.modules[classRef.name] = classRef

    def VersionCheck(self, version):
        return self.version == version

    def GetModule(self, pModule: Module):
        for key in self.modules:
            mod = self.modules[key]
            if issubclass(pModule, type(mod)):
                return mod