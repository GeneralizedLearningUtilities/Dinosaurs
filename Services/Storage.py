""" Module for defining persistent storage objects """
import collections
from Queue import Queue

#-----------------------------#
# Storage Container Factories #
#-----------------------------#
class BaseStorageContainerFactory(object):
    """ Factory that makes storage containers """
    
    def makeDict(self):
        raise NotImplementedError()

    def makeList(self):
        raise NotImplementedError()

    def makeQueue(self):
        raise NotImplementedError()

    def makeSet(self):
        raise NotImplementedError()

    def initialize(self):
        pass
    
    def teardown(self):
        pass


class LocalStorageContainerFactory(object):
    """ Factory that makes local python objects """
    
    def makeDict(self):
        return {}
    
    def makeList(self):
        return {}

    def makeQueue(self):
        return Queue()

    def makeSet(self):
        return set()


class GoogleAppEngineContainerFactory(object):
    """ Factory that makes local python objects """
    
    def makeDictionary(self):
        return GoogleAppEngineDictionary()
    
    def makeSet(self):
        return GoogleAppEngineList()
    
    def makeList(self):
        return GoogleAppEngineSet()

    def makeQueue(self):
        return GoogleAppEngineQueue()

    # Note: Probably needs init/teardown functions
    # @TODO: Figure out init/teardown needs for GAE

#---------------------------#
# Storage Container Objects #
#---------------------------#
class BaseStorageContainer(object):
    """ A basic storage container class """
    pass

# Google App Engine Containers
# @TODO: Define these
class GoogleAppEnginePersistence(BaseStorageContainer):
    """ Storage in a GAE data structure """
    pass

class GoogleAppEngineDictionary(GoogleAppEnginePersistence):
    """ Storage in a GAE data structure """
    pass

class GoogleAppEngineList(GoogleAppEnginePersistence):
    """ Storage in a GAE data structure """
    pass

class GoogleAppEngineSet(GoogleAppEnginePersistence):
    """ Storage in a GAE data structure """
    pass

class GoogleAppEngineQueue(GoogleAppEnginePersistence):
    """ Storage in a GAE data structure """
    pass
