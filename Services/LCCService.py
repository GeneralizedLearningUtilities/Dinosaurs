from SKO_Architecture.MessagingGateway import BaseService

class LCCService(BaseService):
    """ A service for calculating learner's characteristic curves """
    
    def __init__(self, id=None, publisher=None, data=None, factory=None):
        super(LCCService, self).__init__(id, publisher)
        if data is None: data = DictionaryContainer()
        self._data = data
    
    def receiveMessages(self, messages):
        for message in messages:
            if type(message) == LCCLevelRequest:
                responses = self.processLCCRequest(message)
                self.sendMessages(responses)
            elif type(message) == SemanticSimilarityResponse:
                self.processSimilarityResponse(message)
                
    def processSimilarityResponse(self, message):
        # Unpack message similarity and phrases
        phrase1 = ""
        phrase2 = ""
        value = 0
        # Cache the values
        self._data[(phrase1, phrase2)] = value
        # Once all necessary values are presesent, respond

    def processLCCRequest(self, message):
        # Parse LCCLevelRequest actual, expected, history
        # use self.getLCCValues()
        # Generate LCCLevelResponse message
        response = LCCLevelResponse()
        return response

    def getLCCValues(self, actual, expected, history):
        raise NotImplementedError

    def getNovelty(self, actual, history):
        raise NotImplementedError

    def getRelevance(self, actual, expected):
        raise NotImplementedError

    def getSemanticSimilarity(self, phrase1, phrase2):
        """
        Gets a semantic similarity between two phrases.
        If available in local data, reads that data, otherwise
        sends a request for the semantic similarity value and
        escapes until a new message arrives (which may have the data)
        @param phrase1: First phrase
        @type phrase1: basestring
        @param phrase2: Second phrase
        @type phrase1: basestring
        @return: Semantic similarity between phrases, in [0,1]
        @rtype: float
        """
        if True and (phrase1, phrase2) in self._data:
            return self._data[(phrase1, phrase2)]
        else:
            message = SemanticSimilarityRequest(sender=self, phrase1=phrase1, phrase2=phrase2)
            self.sendMessages([message])
            return None

