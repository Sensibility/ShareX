from .base_module import Module
from .image_module import ImageModule
import os, json

class ModuleLoader(Module):
    modules = []

    def __init__(self):
        dir = os.getcwd() + "/private/config/"
        try:
            f = open(dir + "conf.json", 'r')
        #For the build agent
        except:
            f = open(dir + "conf.orig.json", 'r')

        config = json.loads(str.join("", f.readlines()))
        mods = config.get('Modules')

        if(config.get('Root')):
            self.root = config.get('Root')

        if(mods.get('Images')):
            self.modules.append(ImageModule(mods.get('Images'), self.root))


        f.close()

    def __Get(self, Module):
        for mod in self.modules:
            if(type(mod) is Module):
                return mod

    def GetImage(self):
        return self.__Get(ImageModule)