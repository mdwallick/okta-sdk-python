from okta.models.Link import Link


class FactorCatalogEntry:

    types = {
        'factorType': str,
        'provider': str,
        'status': str,
        'enrollment': str
    }

    dict_types = {
        '_links': Link
    }

    alt_names = {
        '_links': 'links'
    }

    def __init__(self):

        self.factorType = None  # str

        self.provider = None  # str

        self.status = None  # str

        self.enrollment = None  # str

        self.links = None  # Map<String, LinksUnion>
