class FactorProfile:

    types = {
        'question': str,
        'questionText': str,
        'answer': str,
        'phoneNumber': str,
        'credentialId': str,
        'deviceType': str,
        'name': str,
        'platform': str,
        'version': str
    }

    def __init__(self):

        # unique key for question
        self.question = None  # str

        # display text for question
        self.questionText = None  # str

        # answer to question
        self.answer = None  # str

        # phone number of mobile device
        self.phoneNumber = None  # str

        # unique id for instance
        self.credentialId = None  # str

        self.deviceType = None

        self.name = None

        self.platform = None

        self.version = None
