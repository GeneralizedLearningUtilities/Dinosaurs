# -*- coding: utf-8 -*-

class DummyDB(object):
    """
    The dummy DB for unit test 
    """

    #TODO:Specify the DB's accessing info here
    DB_INFO = None

    #Init
    def __init__(self):
        #Knowledge level: [studentID][conceptID] = knowledge level
        self._knowledge = {
            '00125':
                {'Math-1': 0.95, 'Math-2': 0.75, 'Math-3': 0.39, 'Math-4': 0.0},
            '00126':
                {'Math-1': 0.6,  'Math-2': 0.62, 'Math-3': 0.58, 'Math-4': 0.62},
            '00410':
                {'Math-1': 1.0,  'Math-2': 1.0,  'Math-3': 1.0,  'Math-4': 1.0}
            }

        #Knowledge dependency
        #Dependency: [Source Concept ID][Target Concept ID] = weight
        self._dependency = {
            'Math-1':{'Math-2': 0.9},
            'Math-2':{'Math-3': 0.85, 'Math-4': 0.4},
            'Math-3':{'Math-4': 0.6}
            }
