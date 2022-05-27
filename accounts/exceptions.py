from rest_framework.exceptions import APIException


class SellerNotAuthorizedForThisActionException(APIException):
    status_code = 403
    default_detail = "seller not authorized for this action."

    def __init__(self, detail= default_detail , code= status_code):
        self.status_code = code
        super().__init__(detail, code)

class UserAlreadyExistsException(APIException):
    status_code = 409
    default_detail = "A user with such a field already exists."

    def __init__(self, detail= default_detail , code= status_code):
        self.status_code = code
        super().__init__(detail, code)
