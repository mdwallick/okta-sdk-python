from okta.models.factor.Verification import Verification


class FactorUpdateRequest:

    types = {
        'verify': Verification,
        'profile': dict
    }

    def __init__(self):

        self.verify = None  # Verification

        self.profile = None  # Map<String, Object>
