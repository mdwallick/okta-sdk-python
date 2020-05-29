class ActivationResponse:

    types = {
        'activationUrl': str,
        'activationToken': str
    }

    def __init__(self):

        self.activationUrl = None  # str
        self.activationToken = None # str
