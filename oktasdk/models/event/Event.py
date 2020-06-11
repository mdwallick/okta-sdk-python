from datetime import datetime
from oktasdk.models.event.Action import Action
from oktasdk.models.event.Actor import Actor
from oktasdk.models.event.Target import Target


class Event:

    types = {
        'eventId': str,
        'published': datetime,
        'requestId': str,
        'sessionId': str,
        'action': Action,
        'actors': Actor,
        'targets': Target
    }

    def __init__(self):

        # unique key for event
        self.id = None  # str

        # timestamp when event was published  
        self.published = None  # datetime

        # identifies the request
        self.requestId = None  # str

        # session in which the event occurred
        self.sessionId = None  # str

        self.action = None  # Action

        self.actors = None

        self.targets = None
