# -*- coding: utf-8 -*-
import os
import unittest.case
from Student_Model.Concept import (Concept,)
from Util.Paths import getBasePath
from Util.JSInterpreter import executeJS
from Util.Serialization import (StorageToken, Serializable, makeNative, untokenizeObject)

class ConceptTest(unittest.case.TestCase):
    """ Unit test for the Agent class, test all Serializable methods """
    TEST_CLASS = Concept

    def setUp(self):
        """ Create the Agent object to be used in the tests """
        self.concept = self.TEST_CLASS()

    def testChooseActions(self):
        pass

    def testPerceive(self):
        pass

    # Begin of Serializable tests
    def test__init__(self):
        """ Test that the Agent object is being initialized correctly """
        a = self.TEST_CLASS()
        self.assertIsInstance(a, self.TEST_CLASS)
        self.assertTrue(type(a) == self.TEST_CLASS)

    def testSaveToToken(self):
        """ Test that the Agent object is being correctly saved as a Token """
        self.assertIsInstance(self.concept.saveToToken(), StorageToken)

    def testInitializeFromToken(self):
        """ Test that the Agent object is being correctly initialized
        from a Token
        """
        t = self.concept.saveToToken()
        c = self.TEST_CLASS("Name")
        self.assertNotEqual(c, self.concept)
        c.initializeFromToken(t)
        self.assertEqual(c, self.concept)

    def testCreateFromToken(self):
        """ Test that the Agent object is being correctly created
        from a Token
        """
        t = self.concept.saveToToken()
        c = Serializable.createFromToken(t)
        self.assertEqual(c, self.concept)

    def testReadFromJSObject(self):
        """ Test that we can read the JS equivalent of this class into this object """
        try:
            dirPath = os.path.dirname(__file__)
            sObj = executeJS("Concept_concept.js", dirPath + os.sep, getBasePath())
        except NameError:
            sObj = executeJS("Concept_concept.js", '', getBasePath())
        token = makeNative(sObj)
        x = untokenizeObject(token)
        self.assertIsInstance(x, self.TEST_CLASS)
        self.assertEqual(type(x), self.TEST_CLASS)
        self.assertEqual("conceptId", x.getConceptId())
        self.assertEqual("name", x.getName())
        self.assertEqual("description", x.getDescription())
    # End of Serializable tests

if __name__ == "__main__":
    unittest.main()
