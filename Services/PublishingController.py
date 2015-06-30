from Util.Serialization import JSON_FORMAT

class BasePublishingController(object):
    """ A generic publishing controller class """
    def __init__(self, id=None, relays=None, services=None):
        super(BasePublishingController, self).__init__(id)
        if services is None: services = []
        if relays is None: relays = []
        self._services = dict([(service.getId(), service) for service in services])
        self._messageQueue = []
        self._deliveryQueue = []
        self._messageLock = False
        self._deliveryLock = False

    # Abstract methods - Need to be defined
    def findMessageTargets(self, sender, message):
        """
        Use rules to determine who should receive a copy of each message.
        """
        raise NotImplementedError

    # Receive Messages (Broadcast Inputs)
    def receiveMessage(self, message):
        self._messageQueue.append(message)

    def receiveMessages(self, messages):
        self._messageQueue.extend(messages)

    # Deliver Messages (Outputs)
    def deliverNext(self):
        if self._deliveryQueue:
            self.forceDeliver(*self._deliveryQueue.pop(0))

    def forceDeliverMessage(self, target, message):
        """ Push a message out to a particular target """
        target.receiveMessages([message])

    def forceDeliverMessages(self, target, messages):
        """ Push a message out to a particular target """
        target.receiveMessages(message)

    # Post Messages (Relay Outputs)
    def receiveDelivery(self, target, message):
        """ Receive a delivery from some other controller """
        self._deliveryQueue.append((target, message))

    def relayDelivery(self, target, message):
        pass

    # Process Messages (Switchboard)
    def processNext(self):
        """ Determine and cache the targets for a message """
        if self._messageQueue:
            self.processMessage(*self._messageQueue.pop(0))

    def processMessage(self, sender, message):
        """ Determine and cache the targets for a message """
        targets = self.findMessageTargets(sender, message)
        self._deliveryQueue.extend([(target, message) for target in targets])

    def flushMessages(self):
        """ Process and deliver all messages in the queue """
        while len(self._messages) > 0:
            self.processNext()
        while len(self._deliveryQueue) > 0:
            self.deliverNext()


class RelayPublishingController(object):
    """
    Controller that only provides relays
    """
    pass
