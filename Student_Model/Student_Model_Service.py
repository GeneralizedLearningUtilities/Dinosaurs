# -*- coding: utf-8 -*-

from SKO_Architecture.MessagingGateway import BaseService

class StudentModelService(BaseService):

    def __init__(self, anId=None, gateway=None):
        super(StudentModelService, self).__init__(anId, gateway)

    def getStudentKnowledge(self, studentId, concept):
        return 0

    def _cacheStudentKnowledge(self):
        pass
