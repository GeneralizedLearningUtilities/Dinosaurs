
class RequestManager(object):
    """ A manager that handles sequences of requests """
    def __init__(self, active=None, waiting=None, requirements=None):
        if active is None: active = DictionaryContainer()
        if waiting is None: waiting = DictionaryContainer()
        self._activeRequests = []
        self._waitingRequests = {}
        self._requirements = requirements
