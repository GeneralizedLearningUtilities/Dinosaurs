# -*- coding: utf-8 -*-

from DummyDB import DummyDB
from KnowledgeModel import BaseKnowledgeModel

class KnowledgeGraph(object):
    """
    This is the class that represents connections between knowledge concepts
    and supports the functions to access those connections (dependencies).
    """

    #Init
    def __init__(self):
        #Knowledge dependency
        #Dependency: [Source Concept ID][Target Concept ID] = weight
        self._dependency = {}

        #Observers (type of knowledge model)
        self._observers = []

    def setDependency(self, dependency):
        self._dependency = dependency

    def getDependency(self):
        return self._dependency

    #Accessors -- Read-Only for users
    def getDependency(self, sourceID = None, targetID = None):
        if (sourceID == None or targetID == None):
            raise ValueError("Input source concept id or target concept id is invalid!")

        if (self._dependency.get(sourceID) == None):
            return None
        else:
            return self._dependency.get(sourceID).get(targetID);
        
    def getDependencyBySource(self, sourceID = None):
        # Return all dependencies which start by input sourceID 
        if (sourceID == None):
            raise ValueError("Input source concept id is invalid!")

        rt = {}
        rt[sourceID] = self._dependency.get(sourceID)
        return rt
    
    def getDependencyByTarget(self, targetID = None):
        # Return all dependencies which end with input targetID 
        if (targetID == None):
            raise ValueError("Input target concept id is invalid!")

        rt = {}
        keys = self._dependency.keys()
        for key in keys:
            if (self._dependency.get(key).get(targetID)):
                rt[key] = {}
                rt[key][targetID] = self._dependency.get(key).get(targetID)
                
        return rt

    def getAllDependencies(self):
        return self._dependency

    def getParents(self, currentID = None):
        if (currentID == None):
            raise ValueError("Input current concept id is invalid!")

        rt = []
        childSet = []
        childSet.append(currentID)
        keys = self._dependency.keys()

        while (childSet):
            currentChild = childSet.pop()
            rt.append(currentChild)
            
            for key in keys:
                if (self._dependency.get(key).get(currentChild) and key not in rt):
                    childSet.append(key)

        rt.remove(currentID)
        return rt

    
    #Modifiers -- For admins
    def updateDependency(self, sourceID = None, targetID = None, weight = None):
        #Updating the existing dependency's weight
        if (sourceID == None or targetID == None):
            raise ValueError("Input source concept id or target concept id is invalid!")

        if (weight == None):
            raise ValueError("Input weight is invalid!")

        if (self._dependency.get(sourceID) != None and self._dependency.get(sourceID).get(targetID) != None):
            #Update the weight
            self._dependency[sourceID][targetID] = weight
            return True
        else:
            raise ValueError("The requested dependency is not available. Using 'addDependency' to create new one.")
        
    def addDependency(self, sourceID = None, targetID = None, weight = None, acyclicCKFlag = False):
        #Creating a new dependency. May or may not need to do an acyclic check
        
        if (sourceID == None or targetID == None):
            raise ValueError("Input source concept id or target concept id is invalid!")

        if (weight == None):
            raise ValueError("Input weight is invalid!")

        if (self._dependency.get(sourceID) != None and self._dependency.get(sourceID).get(targetID) != None):
            raise ValueError("The requested dependency is already available. Using 'updateDependency' to change its weight.")
        else:
            if (acyclicCKFlag == True and acyclicCK(sourceID, targetID) == False):
                raise ValueError("The requested dependency is invalid. It makes the acyclic graph cyclic.")
            else:
                #Create a new dependency
                if (self._dependency.get(sourceID) == None):
                    self._dependency[sourceID] = {}
                self._dependency[sourceID][targetID] = weight
                return True
                        
    def delDependency(self, sourceID = None, targetID = None):
        #Deleting the existing dependency
        if (sourceID == None or targetID == None):
            raise ValueError("Input source concept id or target concept id is invalid!")

        if (self._dependency.get(sourceID) != None and self._dependency.get(sourceID).get(targetID) != None):
            # Delete the dependency
            del self._dependency[sourceID][targetID]
            if (self._dependency.get(sourceID) == None):
                del self._dependency[sourceID]
                return True
        else:
            raise ValueError("The requested dependency is not available. No need to delete.")

    def acyclicCK(self, sourceID = None, targetID = None):
        # Check one graph's acyclic ability when adding a new dependency
        # True --> acyclic; False --> not acyclic

        #Create a new dependency
        newDependency = self._dependency
        if (newDependency.get(sourceID) == None):
            newDependency[sourceID] = {}
        newDependency[sourceID][targetID] = 1.0

        # Algorithm for checking: A topological sort
        """
        Pseudo code:
        Q <-- Set of all nodes with no incoming edges
        while Q is non-empty do
            remove a node n from Q
            for each node m with an edge e from n to m do
                remove edge e from the graph
                if m has no other incoming edges then
                    insert m into Q
        if graph has edges then
            output error message (graph has a cycle)
        else 
            output correct message (graph doesn't has a cycle)
        """
        # TODO:Implement above algo
        
        return True


    #Obsering pattern
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
                
    def updateConcept(self):
        #Inform the observers
        for observer in self._observers:
            observer.initGraph(self) # Pass KG itself to its observers, including its graph data and the methods


#Test cases
if __name__ == '__main__':
    print "--Start Test--"

    TMP_DB = DummyDB()
    
    print "DB's original content is:"
    print TMP_DB._dependency

    KG = KnowledgeGraph()

    #Get student's knowledge from DB
    KG._dependency = TMP_DB._dependency

    #Usual cases
    graph = KG.getAllDependencies()
    print "The all dependencies in Knowledge Graph are:"
    print graph

    weight1 = KG.getDependency('Math-2', 'Math-3')
    print "The weight between 'Math-2' and 'Math-3' is:"
    print weight1

    s1 = KG.getDependencyBySource('Math-2')
    print "The all target concepts which start from 'Math-2' are:"
    print s1

    t1 = KG.getDependencyByTarget('Math-4')
    print "The all source concepts which end by 'Math-4' are:"
    print t1

    parents = KG.getParents('Math-4')
    print "The parents concepts of 'Math-4' are:"
    print parents

    KG.updateDependency('Math-2', 'Math-3', 0.95)
    weight2 = KG.getDependency('Math-2', 'Math-3')
    print "The updated weight between 'Math-2' and 'Math-3' is:"
    print weight2

    weight3 = KG.getDependency('Math-1', 'Math-4')
    print "The weight between 'Math-1' and 'Math-4' is (non-available yet):"
    print weight3
    KG.addDependency('Math-1', 'Math-4', 0.4)
    weight3 = KG.getDependency('Math-1', 'Math-4')
    print "New created weight between 'Math-1' and 'Math-4' is:"
    print weight3

    KG.delDependency('Math-2', 'Math-3')
    weight4 = KG.getDependency('Math-2', 'Math-3')
    print "The weight between 'Math-2' and 'Math-3' is (has been deleted):"
    print weight4

    TMP_DB._dependency = KG._dependency
    
    print "DB's new content is:"
    print TMP_DB._dependency

    #Unusual cases (Error should be arised for each of cases below if open the comment)
    #Update non-available dependency
    #KG.updateDependency('Math-2', 'Math-1', 1.0)

    #Add a repeated dependency
    #KG.addDependency('Math-1', 'Math-2', 1.0)

    #Delete an non-available dependency
    #KG.delDependency('Math-4', 'Math-2')
    
    print "--End of test--"


















    
    
        
