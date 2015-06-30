# -*- coding: utf-8 -*-

from DummyDB import DummyDB
from KnowledgeModel import BaseKnowledgeModel

class BaseKnowledgeLevel(object):
    """
    This is the class that supports the functions to calculate
    and access studens' knowledge level
    """
    ALEKS_LEVEL = 0.8
    ALEKS_LAMBDA = 0.5

    #Init
    def __init__(self):
        #Estimated knowldge
        #Knowledge: [conceptID] = knowledge level
        self._knowledge = {}

        #Observers (type of knowledge model)
        self._observers = []

        #ALEKS sorce
        self._aleks = self.ALEKS_LEVEL

        #ALEKS_LAMBDA
        self._aleks_lambda = self.ALEKS_LAMBDA
        
    def setKnowledge(self, knowledge = None):

        #The input knowledge is possible to be None
        #if the student doesn't has any past records.
        self._knowledge = knowledge
        
    def getKnowledge(self):
        return self._knowledge
    
    def getKnowledgeLevel(self, conceptID = None):
        if (conceptID == None):
            raise ValueError("Input concept id is not available!")

        kl = 0
        if (self._knowledge.get(conceptID) != None):
            kl = self._knowledge.get(conceptID)

        return kl * self._aleks_lambda + self._aleks * (1 - self._aleks_lambda)
    
    def setKnowledgeLevel(self, conceptID = None, level = None):
        if (conceptID == None):
            raise ValueError("Input concept id is not available!")

        if (level == None):
            raise ValueError("Input knowledge level is not available!")

        self._knowledge[conceptID] = level

    def getALEKS(self):
        return self._aleks

    def setALEKS(self, aleks = None):
        if (aleks == None):
            raise ValueError("Input ALEKS score is not available!")

        self._aleks = aleks

    def getALEKSLambda(self):
        return self._aleks_lambda

    def setALEKSLambda(self, aleks_lambda = None):
        if (aleks_lambda == None):
            raise ValueError("Input ALEKS LAMBDA score is not available!")

        self._aleks_lambda = aleks_lambda

    def addObserver(self, observer = None):
        if (observer == None):
            raise ValueError("Input observer is not available!")

        if (isinstance (observer, BaseKnowledgeModel)):
            if not observer in self._observers:
                self._observers.append(observer)     
        else:
            raise TypeError("Input is not an acceptable type of observer(knowledge model)!")

    def removeObserver(self, observer = None):
        if (observer == None):
            raise ValueError("Input observer is not available!")

        try:
            if observer in self._observers:
                self._observers.remove(observer)
        except ValueError:
            pass
                
    def updateKnowledge(self, conceptID = None, obsEst = None):
        if (conceptID == None):
            raise ValueError("Input conceptID is not available!")

        if (obsEst == None):
            raise ValueError("Input estimated knowledge is not available!")

        #Update the KL
        self.setKnowledgeLevel(conceptID, obsEst)

        #Need to use method 'getKnowledgeLevel' to reflect the impact of ALEKS
        currentEst = self.getKnowledgeLevel(conceptID)

        #Inform the observers
        for observer in self._observers:
            observer.update(conceptID, currentEst)


class DecayKnowledgeLevel(BaseKnowledgeLevel):
    """
    This is a sub class of BaseKnowledgeLevel. It supports a certain updateKnowledge
    method which calculate the estimated knowledge level with the past experience.
    """
    DECAY_LAMBDA = 0.5
    
    #Init
    def __init__(self):
        super(DecayKnowledgeLevel, self).__init__()

        self._decay_lambda = self.DECAY_LAMBDA

    def getDecayLambda(self):
        return self._decay_lambda

    def setDecayLambda(self, decay_lambda = None):
        if (decay_lambda == None):
            raise ValueError("Input ALEKS LAMBDA score is not available!")

        self._decay_lambda = decay_lambda

    def updateKnowledge(self, conceptID = None, obsEst = None):
        if (conceptID == None):
            raise ValueError("Input conceptID is not available!")

        if (obsEst == None):
            raise ValueError("Input estimated knowledge is not available!")

        #Update the KL
        #Don't use method 'self.getKnowledgeLevel()',
        #because the impact of ALEKS is not necessary here.
        pastEst = self._knowledge.get(conceptID)

        if (pastEst == None):
            self.setKnowledgeLevel(conceptID, obsEst)
        else:
            decayedEst = self.linearEstimation(pastEst, obsEst)
            self.setKnowledgeLevel(conceptID, decayedEst)

        #Need to use method 'getKnowledgeLevel' to reflect the impact of ALEKS
        currentEst = self.getKnowledgeLevel(conceptID)
        #Inform the observers
        for observer in self._observers:
            observer.update(conceptID, currentEst)

    def linearEstimation(self, pastE = None, obsE = None):
        return self._decay_lambda*pastE + (1 - self._decay_lambda)*obsE
   
     
#Test cases
if __name__ == '__main__':
    print "--Start Test--"

    tmpDB = DummyDB()

    studentKL = {}
    studentKL = tmpDB._knowledge.get('00125')

    print studentKL

    KL = DecayKnowledgeLevel()

    KL.setKnowledge(studentKL)
    print KL.getKnowledgeLevel('Math-3')

    newKL = {}
    newKL = KL.getKnowledge()

    print newKL

    print "--End of test--"
    
    
    
