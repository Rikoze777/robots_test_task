import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from orders.services import add_order, check_order, save_order
from django.core.exceptions import ValidationError


@csrf_exempt
@require_http_methods(['POST'])
def create_order(request):
    try:
        data = json.loads(request.body)
        customer, serial = add_order(data)
        existing_order = check_order(customer, serial)
        if existing_order:
            return JsonResponse({'message': 'Заказ уже принят. Ожидайте поступления робота'})
        else:
            save_order(customer, serial)
            return JsonResponse({'message': 'Заказ успешно принят'})
    except ValidationError as err:
        return JsonResponse({'message': str(err)}, status=400)
    except Exception as err:
        return JsonResponse({'message': 'An error occurred'}, status=500)
