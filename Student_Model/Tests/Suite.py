# -*- coding: utf-8 -*-
import unittest
import Student_Model.Tests.Concept_UnitTests as Concept_UnitTests

def TestSuite():
    """
    Returns a TestSuite object that covers the Util module
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    modules = [Concept_UnitTests]
    for m in modules:
        suite.addTests(loader.loadTestsFromModule(m))
    return suite


if __name__ == "__main__":
    import sys
    sys.exit(not unittest.TextTestRunner().run(TestSuite()))
