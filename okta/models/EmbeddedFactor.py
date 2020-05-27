from okta.models.Link import Link


class EmbeddedFactor:

    types = {
        'timeStep': int,
        'sharedSecret': str,
        'encoding': str,
        'keyLength': int,
        'factorResult': str,
        'links': dict
    }

    dict_types = {
        '_links': Link
    }

    alt_names = {
        '_links': 'links'
    }

    def __init__(self):

        self.timeStep = None

        self.sharedSecret = None

        self.encoding = None

        self.keyLength = None

        self.factorResult = None

        self.links = None
