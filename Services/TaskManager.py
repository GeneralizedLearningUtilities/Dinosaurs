import uuid
from Queue import Empty
from abc import ABCMeta, abstractmethod
from SKO_Architecture.Messaging import Message
from SKO_Architecture.Services.Storage import LocalStorageContainerFactory


class TaskSpecification(object):
    """
    A specified task that has a method to initiate when ready,
    some list of provided arguments, and some requirements.
    """
    ERROR_STATUS = -1
    WAITING_STATUS = 0
    EVALUATING_STATUS = 1
    DISPATCHED_STATUS = 2
    
    def __init__(self, method, args=None, reqs=None, taskId=None):
        """
        Description of a task that needs to be completed.
        @param method: Method that the task calls
        @type method: callable
        @param args: Keyword arguments available to the task
        @type args: dict of {str : object}
        @param reqs: Required keyword arguments not available
        @type reqs: dict of {str : requirement}
        @param taskId: Unique id for the task
        @type taskId: uuid
        """
        if not args: args = {}
        if not reqs: reqs = {}
        if taskId is None: taskId = uuid.uuid4()
        self._id = taskId
        self._method = method
        self._arguments = args
        self._requirements = reqs
        self._status = self.WAITING_STATUS

    def getId(self):
        """ Get the ID for the task """
        return self._id

    def getRequirements(self):
        """ List the requirements that this task needs """
        return set(self._requirements.values())

    def getStatus(self):
        """ Get the status of the task """
        return self._status

    def resetStatus(self):
        """ Reset the status to waiting """
        self._status = self.WAITING_STATUS

    def __call__(self, requiredItems=None):
        """
        Evaluate the task
        @param requiredItems: Mapping of requirement specifications to their values
        @type requiredItems: {Message : Value}
        @return: Return the status of this task.  Should be DISPATCHED_STATUS when done.
        @rtype: int
        """
        if requiredItems is None: requiredItems = {}
        if self._status == self.WAITING_STATUS:
            kwds = dict(self._arguments)
            for name, req in self._requirements.iteritems():
                kwds[name] = requiredItems[req]
            self._status = self.EVALUATING_STATUS
            try:
                self._method(**kwds)
            except Exception:
                self._status = self.ERROR_STATUS
                raise
            self._status = self.DISPATCHED_STATUS
        return self._status
    

class TaskDispatcher(object):
    """
    A general task dispatcher that relies on task queues and
    a requirement map for pushing tasks out.
    """
    SEND_REQUIREMENT_ACTION = "Sent Requirement"
    DISPATCHED_TASK_ACTION = "Dispatched Task"
    PROCESSED_REQ_ACTION = "Processed Requirement"

    def __init__(self, tasks=None, dataFactory=None):
        if tasks is None: tasks = []
        if dataFactory is None: dataFactory = LocalStorageContainerFactory()
        self._dataFactory = dataFactory
        self._taskIdMap = self._makeMap()
        self._readyTasks = self._makeQueue()
        self._newRequirements = self._makeQueue()
        self._receivedRequirements = self._makeQueue()
        self._requirementMap = self._makeRequirementMap()
        for task in tasks:
            self.addTask(task)

    # Start storage interfaces/containers
    def _makeMap(self):
        return self._dataFactory.makeDict()
    
    def _makeQueue(self):
        return self._dataFactory.makeQueue()

    def _makeRequirementMap(self):
        return RequirementMap(self._dataFactory)

    # State Management
    #def clear(self):
    #    pass

    # Task Accessors
    def getTask(self, taskId):
        return self._taskIdMap[taskId]
    
    def addTask(self, task, errorOnDuplicate=False):
        """
        Receive a task to execute
        NOTE: This happens on-event, so it needs to be fast.
        """
        taskId = task.getId()
        if taskId not in self._taskIdMap:
            self._taskIdMap[taskId] = task
            taskReqs = task.getRequirements()
            filledReqs = self._requirementMap.fillRequirements(taskReqs)
            # If everything filled, put in the ready tasks list
            if len(filledReqs) == len(taskReqs):
                self._readyTasks.put((taskId, filledReqs))
            # Otherwise, add to waiting tasks and register requirements
            else:
                newRequirements = self._requirementMap.addTask(task.getId(), taskReqs)
                for req in newRequirements:
                    self._newRequirements.put(req)
        elif errorOnDuplicate:
            raise KeyError("Duplicate task added: %s"%(taskId,))

    def _dispatchNextTask(self):
        try:
            taskId, requirements = self._readyTasks.get_nowait()
        except Empty:
            return
        task = self._taskIdMap[taskId]
        del self._taskIdMap[taskId]
        task(requirements)
        
    # Requirement Accessors
    def isValidRequirementMessage(self, message):
        return True

    def makeCanonicalMessage(self, message):
        """ Remove irrelevant information to make message canonical """
        return message
    
    def _sendNextRequirement(self):
        try:
            requirement = self._newRequirements.get_nowait()
        except Empty:
            return
        # Send a message requesting the required value here
        
    def receiveRequirement(self, message):
        """
        Receive a message that could carry required data
        NOTE: This happens on-event, so it needs to be fast.
        """
        message = self.makeCanonicalMessage(message)
        if self.isValidRequirementMessage(message):
            self._receivedRequirements.put(message)
            
    def _processNextReceivedRequirement(self):
        try:
            message = self._receivedRequirements.get_nowait()
        except Empty:
            return
        value = message.getResult()
        req = message.getRequest()
        waitingTaskIds = self._requirementMap.getTasksWithRequirement(req)
        if len(waitingTaskIds) > 0:
            self._requirementMap.setRequirementValue(req, value)
            tasksReady = [taskId for taskId in waitingTaskIds if
                          self._requirementMap.isTaskReady(taskId)]
            for taskId in tasksReady:
                requirements = self._requirementMap.getTaskRequirementValues(taskId)
                self._requirementMap.removeTask(taskId)
                self._readyTasks.put((taskId, requirements))

    # Execution Flow
    def doAction(self):
        if self._newRequirements.qsize() > 0:
            self._sendNextRequirement()
            return self.SEND_REQUIREMENT_ACTION
        elif self._readyTasks.qsize() > 0:
            self._dispatchNextTask()
            return self.DISPATCHED_TASK_ACTION
        elif self._receivedRequirements.qsize() > 0:
            self._processNextReceivedRequirement()
            return self.PROCESSED_REQ_ACTION
        else:
            return None

    def run(self, runWhenIdle=False):
        hasAction = True
        while hasAction or runWhenIdle:
            hasAction = self.doAction()


class RequirementMap(object):
    """
    A bidirectional map of tasks to requirements,
    with a map of requirements to known values.
    """
    def __init__(self, dataFactory=None):
        if dataFactory is None: dataFactory = LocalStorageContainerFactory()
        self._dataFactory = dataFactory
        self._taskReqs = self._makeMap()
        self._tasksByReq = self._makeMap()
        self._reqValues = self._makeMap()

    #def clear(self):
    #    pass
        
    def _makeMap(self):
        return self._dataFactory.makeDict()

    def _makeSet(self):
        return self._dataFactory.makeSet()

    def addTask(self, taskId, taskReqs, errorOnDuplicate=False):
        if taskId not in self._taskReqs:
            taskReqsSet = self._makeSet()
            taskReqsSet.update(taskReqs)
            self._taskReqs[taskId] = taskReqsSet
            newReqs = set()
            for req in taskReqs:
                if req not in self._tasksByReq:
                    self._tasksByReq[req] = self._makeSet()
                    newReqs.add(req)
                self._tasksByReq[req].add(taskId)
            return newReqs
        elif errorOnDuplicate:
            raise KeyError("Duplicate taskId found in requirements map: %s"%(taskId))
        return set()

    def removeTask(self, taskId):
        reqs = self._taskReqs[taskId]
        del self._taskReqs[taskId]
        for req in reqs:
            if len(self._tasksByReq[req]) == 1:
                del self._tasksByReq[req]
                if req in self._reqValues:
                    del self._reqValues[req]
            else:
                self._tasksByReq[req].remove(taskId)

    def getRequirementsForTask(self, taskId):
        return self._taskReqs[taskId]

    def getTasksWithRequirement(self, req):
        return self._tasksByReq.get(req,set())

    def setRequirementValue(self, req, value):
        self._reqValues[req] = value

    def isTaskReady(self, taskId):
        reqs = self._taskReqs[taskId]
        unfilledReqs = [req for req in reqs if req not in self._reqValues]
        return len(unfilledReqs) == 0
    
    def getTaskRequirementValues(self, taskId):
        return dict([(req, self._reqValues[req]) for req in self._taskReqs[taskId]])

    def fillRequirements(self, reqs, errorOnUnfilled=False):
        if errorOnUnfilled:
            return dict([(req, self._reqValues[req]) for req in reqs])
        else:
            return dict([(req, self._reqValues[req]) for req in reqs if req in self._reqValues])

