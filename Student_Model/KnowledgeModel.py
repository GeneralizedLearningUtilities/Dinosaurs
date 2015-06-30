# -*- coding: utf-8 -*-

class BaseKnowledgeModel(object):
    """
    This is a kind of abstract class, which is used to represent knowledge
    model for calculating the estimated knowledge level by a certain algorithm.
    This class must be inherited 
    """

    #Init
    def __init__(self):
        #Estimated knowldge
        #Knowledge: [conceptID] = knowledge level
        #This variable follows KL
        self._knowledge = {}

        #Knowledge dependency, which includes data and methods on it
        #Dependency data: [Source Concept ID][Target Concept ID] = weight
        self._KG = None

    # Accessing the whole knowledge
    def getKnowledge(self):
        return self._knowledge
    
    def setKnowledge(self, knowledge = None):
        self._knowledge = knowledge
    
    #Accessing KnowledgeLevel
    def getKnowledgeLevel(self, conceptID):
        return self._knowledge.get(conceptID)

    def setKnowledgeLevel(self, conceptID, level):
        self._knowledge[conceptID] = level

    #Update 
    def update(self, conceptID, level):
        print "[BaseKnowledgeModel] Update."
        self.setKnowledgeLevel(conceptID, level)

    def initGraph(self, KG = None):
        print "[BaseKnowledgeModel] InitGraph."
        self._KG = KG


class PointKnowledgeModel(BaseKnowledgeModel):
    """
    This is a sub class of BaseKnowledgeModel. This class calculate the
    estimated knowledge level by using the knowledge level of an independent concept
    """

    #Init
    def __init__(self):
        #Inherit super class's attributes
        super(PointKnowledgeModel, self).__init__()

    #All behaviors are same to that of BaseKnowledgeModel


class DependentKnowledgeModel(BaseKnowledgeModel):
    """
    This is a sub class of BaseKnowledgeModel. This class calculate the
    estimated knowledge level by using the knowledge level of concepts
    and their dependency
    Note that this class is an abstract class, which is must be inherited
    """

    def __init__(self):
        #Inherit super class's attributes
        super(DependentKnowledgeModel, self).__init__()

    def getKnowledgeLevel(self, conceptID = None):
        raise NotImplementedError


class MinDependentKnowledgeModel(DependentKnowledgeModel):
    """
    This is a sub class of DependentKnowledgeModel. This class calculate the
    estimated knowledge level by using minimal knowledge level within the input concept
    and its parents
    """

    def __init__(self):
        #Inherit super class's attributes
        super(MinDependentKnowledgeModel, self).__init__()

    #Override
    def getKnowledgeLevel(self, conceptID = None):
        if (conceptID == None):
            raise ValueError("Input concept id is not available!")

        #Search all parents of the conceptID and return their minimal level as result
        parentsConcept = self._KG.getParents(conceptID)

        #Get the minimal knowledge level
        minLevel = self._knowledge.get(conceptID)
        for c in parentsConcept:
            kl = self._knowledge.get(c)
            if (kl and kl < minLevel):
                minLevel = kl

        return minLevel
        
class SpreadingActivationKnowledgeModel(BaseKnowledgeModel):
    """
    This is a sub class of BaseKnowledgeModel. This class calculate the
    estimated knowledge level by using the idea of Spreading Activation
    TODO: Implement this class in details
    """

    def __init__(self):
        #Inherit super class's attributes
        super(SpreadingActivationKnowledgeModel, self).__init__()

    #TODO: Implementation

class BayesianKnowledgeModel(BaseKnowledgeModel):
    """
    This is a sub class of BaseKnowledgeModel. This class calculate the
    estimated knowledge level by using the idea of Bayesian
    TODO: Implement this class in details
    """

    def __init__(self):
        #Inherit super class's attributes
        super(BayesianKnowledgeModel, self).__init__()

    #TODO: Implementation

#Test cases
if __name__ == '__main__':
    print "--Start Test--"


    print "--End of test--"
    
