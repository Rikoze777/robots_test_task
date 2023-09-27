from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from robots.utils.ex_serilializers import ReturnDict, ReturnList
from robots.utils import status


def _get_error_details(data, default_code=None):

    if isinstance(data, (list, tuple)):
        ret = [
            _get_error_details(item, default_code) for item in data
        ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: _get_error_details(value, default_code)
            for key, value in data.items()
        }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    text = force_str(data)
    code = getattr(data, 'code', default_code)
    return ErrorDetail(text, code)


def _get_codes(detail):
    if isinstance(detail, list):
        return [_get_codes(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_codes(value) for key, value in detail.items()}
    return detail.code


def _get_full_details(detail):
    if isinstance(detail, list):
        return [_get_full_details(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_full_details(value) for key, value in detail.items()}
    return {
        'message': detail,
        'code': detail.code
    }


class ErrorDetail(str):

    code = None

    def __new__(cls, string, code=None):
        self = super().__new__(cls, string)
        self.code = code
        return self

    def __eq__(self, other):
        result = super().__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        try:
            return result and self.code == other.code
        except AttributeError:
            return result

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __repr__(self):
        return 'ErrorDetail(string=%r, code=%r)' % (
            str(self),
            self.code,
        )

    def __hash__(self):
        return hash(str(self))


class APIException(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)

    def __str__(self):
        return str(self.detail)

    def get_codes(self):
        """
        Return only the code part of the error details.

        Eg. {"name": ["required"]}
        """
        return _get_codes(self.detail)

    def get_full_details(self):
        """
        Return both the message & code parts of the error details.

        Eg. {"name": [{"message": "This field is required.", "code": "required"}]}
        """
        return _get_full_details(self.detail)


# The recommended style for using `ValidationError` is to keep it namespaced
# under `serializers`, in order to minimize potential confusion with Django's
# built in `ValidationError`. For example:
#
# from rest_framework import serializers
# raise serializers.ValidationError('Value was invalid')

# class ValidationError(APIException):
#     status_code = status.HTTP_400_BAD_REQUEST
#     default_detail = _('Invalid input.')
#     default_code = 'invalid'
#     default_params = {}

#     def __init__(self, detail=None, code=None, params=None):
#         if detail is None:
#             detail = self.default_detail
#         if code is None:
#             code = self.default_code
#         if params is None:
#             params = self.default_params

#         # For validation failures, we may collect many errors together,
#         # so the details should always be coerced to a list if not already.
#         if isinstance(detail, str):
#             detail = [detail % params]
#         elif isinstance(detail, ValidationError):
#             detail = detail.detail
#         elif isinstance(detail, (list, tuple)):
#             final_detail = []
#             for detail_item in detail:
#                 if isinstance(detail_item, ValidationError):
#                     final_detail += detail_item.detail
#                 else:
#                     final_detail += [detail_item % params if isinstance(detail_item, str) else detail_item]
#             detail = final_detail
#         elif not isinstance(detail, dict) and not isinstance(detail, list):
#             detail = [detail]

#     def __call__(self, detail, code):
#         self.detail = _get_error_details(detail, code)
#         return self.detail
