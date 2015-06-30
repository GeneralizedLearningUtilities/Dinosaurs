# -*- coding: utf-8 -*-

from Util.Serialization import Serializable

class Concept(Serializable):
    """
    A concept related to some subject matter.
    """
    
    def __init__(self, conceptId=None, name=None, description=None):
        super(Concept, self).__init__()
        self._conceptId = conceptId
        self._name = name
        self._description = description

    def __eq__(self, other):
        return (type(self) == type(other) and
                self._conceptId == other._conceptId and
                self._name == other._name and
                self._description == other._description)

    def __ne__(self, other):
        return not self.__eq__(other)

    def getName(self):
        return self._name
    
    def getConceptId(self):
        return self._conceptId
    
    def getDescription(self):
        return self._description

    def saveToToken(self):
        token = super(Concept, self).saveToToken()
        token["conceptId"] = self._conceptId
        token["name"] = self._name
        token["description"] = self._description
        return token

    def initializeFromToken(self, token, context=None):
        super(Concept, self).initializeFromToken(token, context)
        self._conceptId = token["conceptId"]
        self._name = token["name"]
        self._description = token["description"]
