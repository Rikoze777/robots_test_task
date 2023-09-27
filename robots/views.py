import json
from django.http import JsonResponse
from robots.services import save_robot, serialize_obj
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from robots.utils.custom_exceptions import APIException, ErrorDetail


@csrf_exempt
@require_http_methods('POST')
def add_robot(request):
    try:
        robot = json.loads(request.body)
        checked_robot = save_robot(robot)
        serialized_robot = serialize_obj(checked_robot)
        return JsonResponse(status=200, data=serialized_robot,
                            safe=False)
    except ValidationError as val_err:
        errors = val_err.errors()
        details = list(map(map_error_detail, errors))
        raise APIException(details)
    except json.decoder.JSONDecodeError as json_err:
        raise APIException(json_err.msg, "json_error")
    except TypeError:
        raise APIException("Invalid format", "json_error")


def map_error_detail(error):
    return ErrorDetail(error['msg'], error['type'])
