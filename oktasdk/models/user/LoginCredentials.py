from oktasdk.models.user.Provider import Provider
from oktasdk.models.user.Password import Password
from oktasdk.models.user.RecoveryQuestion import RecoveryQuestion


class LoginCredentials:

    types = {
        'password': Password,
        'recovery_question': RecoveryQuestion,
        'provider': Provider
    }

    def __init__(self):

        self.password = None  # Password

        self.recovery_question = None  # RecoveryQuestion

        self.provider = None  # Provider
