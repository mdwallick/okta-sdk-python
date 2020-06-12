from oktasdk.models.usergroup.UserGroupProfile import UserGroupProfile
from oktasdk.models.Link import Link


class UserGroup:

    types = {
        'id': str,
        'type': str,
        'objectClass': str,
        'profile': UserGroupProfile
    }

    dict_types = {
        '_links': Link
    }

    alt_names = {
        '_links': 'links'
    }

    def __init__(self, **kwargs):

        # unique key for group
        self.id = None  # str

        # group type, e.g. OKTA_GROUP
        self.type = None # str

        # determines the groups profile
        self.objectClass = None  # enum

        # the groups profile attributes
        self.profile = None  # UserGroupProfile

        self.links = None

        # Populate profile
        profile_attrs = ['name', 'description']
        for attr in profile_attrs:
            if attr in kwargs:
                self.profile = self.profile or UserGroupProfile()
                setattr(self.profile, attr, kwargs[attr])