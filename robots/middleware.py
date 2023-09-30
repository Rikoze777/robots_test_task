from django.http import JsonResponse
from robots.utils.custom_exceptions import APIException


class CustomErrorMiddlaware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if type(exception) == APIException:
            return JsonResponse(status=400, data=exception.get_full_details(),
                                safe=False)
