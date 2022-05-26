from rest_framework.exceptions import APIException


class SellerNotAuthorizedForThisActionException(APIException):
    status_code = 403
    default_detail = "seller not authorized for this action."

    def __init__(self, detail= default_detail , code= status_code):
        self.status_code = code
        super().__init__(detail, code)
