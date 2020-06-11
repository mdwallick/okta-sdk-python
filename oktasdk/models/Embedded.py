from oktasdk.models.user.User import User
from oktasdk.models.factor.Factor import Factor


class Embedded:

    types = {
        'user': User,
        'factors': Factor
    }

    def __init__(self):

        self.user = None

        self.factors = None