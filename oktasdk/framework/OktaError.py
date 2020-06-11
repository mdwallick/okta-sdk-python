class OktaError(Exception):

    def __init__(self, error, status_code):
        if error is None:
            error = {}

        Exception.__init__(self, error.get('errorSummary'))

        self.status_code = status_code
        self.error_causes = self.__build_string(error.get('errorCauses'))
        self.error_code = error.get('errorCode')
        self.error_id = error.get('errorId')
        self.error_link = error.get('errorLink')
        self.error_summary = error.get('errorSummary')
    
    def __build_string(self, str_list):
        result = []
        for error in str_list:
            result.append(error['errorSummary'])
        return '\n'.join(result)
