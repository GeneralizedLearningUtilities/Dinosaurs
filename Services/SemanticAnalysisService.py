from SKO_Architecture.Service import LocalComponent
from SKO_Architecture.Messages.Semantic_Analysis_Messages import (SemanticSimilarityRequest,
                                                                  SemanticSimilarityResponse)


class SemanticAnalysisService(LocalComponent):
    """ A service for calculating learner's characteristic curves """

    # Message handler
    def receiveMessage(self, message):
        if isinstance(message, SemanticSimilarityRequest):
            response = self.processSimilarityRequest(message)
            self.sendMessages([response])

    # Similarity Calculations
    def calcSimilarity(self, phrase1, phrase2):
        return 0

    def processSimilarityRequest(self, message):
        phrase1 = message.getActor()
        phrase2 = message.getObject()
        value = self.calcSimilarity(phrase1, phrase2)
        response = SemanticSimilarityResponse(None, self, phrase1, phrase2, value)
        return value
