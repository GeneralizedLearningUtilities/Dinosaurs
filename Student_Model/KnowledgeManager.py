# -*- coding: utf-8 -*-

import math

from DummyDB import DummyDB
from KnowledgeLevel import BaseKnowledgeLevel, DecayKnowledgeLevel
from KnowledgeModel import BaseKnowledgeModel, PointKnowledgeModel, DependentKnowledgeModel, MinDependentKnowledgeModel
from KnowledgeGraph import KnowledgeGraph

class KnowledgeEstimator(object):
    """
    This is the class that calculates the estimated knowledge level
    based on the student's performance
    """
    #EXPONENT_VAL = math.e # Replace math.e by '1.5' because it is relatively big causing too heavy penalty
    EXPONENT_VAL = 1.5
    
    def __call__(self, hints = None, prompts = None, summary = None, lcc = None):
       
        o = self.estimateByObserving(hints, prompts, summary)

        obsEst = self.estimateByAll(o, lcc)

        return obsEst

    def estimateByObserving(self, hints = None, prompts = None, summary = None):
        #TODO: Figure out the formula to estimate knowledge level based on the performance
        #Using the sigmoid formula to calculate the penalty to estimate the knowledge level
        #based on the observed performance
        # Penalty: y = 1 / (1 + e^(-x))
        x = hints + prompts
        y = 1 / (1 + math.pow(self.EXPONENT_VAL, -x))
        
        y = y*2 -1 # Change range 0.5~1 (0~0.5 is not avaliable) to 0~1.
        
        level = 1 - y

        if (summary == True): # If bottom out summary is true
            level = level/2   # Penalty is to lose half points when reach the 'bottom out summary'

        return level

    def estimateByAll(self, observing = None, LCC = None):
        #TODO: Figure out the formula to integrate all scores together
        # Temporarily return the average value
        return (observing + LCC) /2;


class KnowledgeManager(object):
    """
    This is the class that manages students' performance and update his/her
    estimated knowledge level
    """

    #Init
    def __init__(self, KL = None, KM = None):

        #student KL (knowledge level)
        if (KL == None):
            self._KL = DecayKnowledgeLevel()
        else:
            self._KL = KL

        #student KM (knowledge model)
        if (KM == None):
            self._KM = PointKnowledgeModel()
        else:
            self._KM = KM

        #Knowledge graph
        self._KG = KnowledgeGraph()

        #Knowledge level of DB
        self._knowledgeLevel = {}

        #Knowledge graph of DB
        #This variable is for every student
        self._knowledgeGraph = {}

        #Temporary DB
        self.tmpDB = DummyDB()

        #An estimator which is used for calculate estimated KL based on the performance
        self._estimator = KnowledgeEstimator()

        #Bind a KM to the KL as its observer
        self._KL.addObserver(self._KM)

        #Bind a KM to the KG as its observer
        self._KG.addObserver(self._KM)

    @classmethod
    def initWithKL(cls, KL = None):
        if (isinstance(KL, BaseKnowledgeLevel)):
            return cls(KL, None)
        else:
            raise TypeError("Input is not an acceptable type of KL(knowledge level) object!")

    @classmethod
    def initWithKM(cls, KM = None):
        if (isinstance(KM, BaseKnowledgeModel)):
            return cls(None, KM)
        else:
            raise TypeError("Input is not an acceptable type of KM(knowledge Model) object!")

    @classmethod
    def initWithKLAndKM(cls, KL = None, KM = None):
        if (isinstance(KL, BaseKnowledgeLevel)):
            if (isinstance(KM, BaseKnowledgeModel)):
                return cls(KL, KM)
            else:
                raise TypeError("Input is not an acceptable type of KM(knowledge Model) object!")
        else:
            raise TypeError("Input is not an acceptable type of KL(knowledge level) object!")

    #Initialize the parameters about KL for a certain student
    def initKnowledgeLevel(self, studentID = None):
        if (studentID == None):
            raise ValueError("Input student Id is not available!")
        
        #Create a knowledge level table for the student
        studentKL = self._knowledgeLevel.get(studentID)
        self._KL.setKnowledge(studentKL)

        #Initialize the estimation in KM
        self._KM.setKnowledge(studentKL)

    #Initialize the parameters about KG
    def initKnowledgeGraph(self):
        self._KG.setDependency(self._knowledgeGraph)
        
        self._KG.updateConcept() #Because KG involves constant values only, its content needs to be update once only
        
    #Pass the ALEKS score
    def setALEKS(self, aleks = None):
        if (aleks == None):
            raise ValueError("Input ALEKS score is not available!")

        self._KL.setALEKS(aleks)
    
    #Save the student's performance and update his/her estimated knowledge level
    def savePerformance(self, studentID = None, conceptID = None, hints = None, prompts = None, summary = None, lcc = None):
        if (studentID == None):
            raise ValueError("Input student Id is not available!")
        
        if (conceptID == None):
            raise ValueError("Input concept Id is not available!")
    
        if (hints == None or hints < 0):
            raise ValueError("Hints value is invalid! (0, 1, 2, ..., n)")

        if (prompts == None or prompts < 0):
            raise ValueError("Prompts value is invalid! (0, 1, 2, ..., n)")

        if (summary != True and summary != False):
            raise ValueError("Prompts value is invalid! (True or False)")

        if (lcc == None or lcc < 0):
            raise ValueError("LCC score value is invalid! (0~1)")

        #Caculate the observed estimation about knowledge level based on the student's performance
        obsEst = self._estimator(hints, prompts, summary, lcc)

        #Update the estimation
        self._KL.updateKnowledge(conceptID, obsEst)

        #Save updated estimation back to the knowledge level table
        #(The table need to be saved back to the DB later)
        self._knowledgeLevel[studentID] = self._KL.getKnowledge()

    def getKnowledgeLevel(self, conceptID = None):
        if (conceptID == None):
            raise ValueError("Input concept id is not available!")

        return self._KM.getKnowledgeLevel(conceptID)

    def loadKnowledgeDB(self):
        #TODO: Replace this temorary DB by real DB
        self._knowledgeLevel = self.tmpDB._knowledge

    def saveKnowledgeDB(self):
        #TODO: Replace this temorary DB by real DB
        self.tmpDB._knowledge = self._knowledgeLevel

    def loadGraphDB(self):
        #TODO: Replace this temorary DB by real DB
        self._knowledgeGraph = self.tmpDB._dependency

    def saveGraphDB(self):
        #TODO: Replace this temorary DB by real DB
        self.tmpDB._dependency = self._knowledgeGraph
    
    
#Test cases
if __name__ == '__main__':
    print "--Start Test--"

    #Default knowledge manager
    km = knowledgeManager()

    #Customized knowledge manager
    #kl = DecayKnowledgeLevel()
    #kmodel = MinDependentKnowledgeModel()
    #km = knowledgeManager.initWithKLAndKM(kl, kmodel)

    km.loadKnowledgeDB()
    km.loadGraphDB()

    km.initKnowledgeLevel('00126')

    km.initKnowledgeGraph()

    km.setALEKS(0.9)

    print "Before to save performance: (00126):"
    print km.getKnowledgeLevel('Math-4')

    km.savePerformance('00126', 'Math-4', 2, 1, False, 0.8)

    print "After to save performance: (00126):"
    print km.getKnowledgeLevel('Math-4')

    km.saveKnowledgeDB()

   
    print "--End of test--"
