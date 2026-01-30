from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def mysite(request):
    hora_atual = timezone.now()
    return render(request, 'myapp/index.html', {'hora_atual': hora_atual})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def registrar_localizacao(request):
    if request.method == "POST":
        data = json.loads(request.body)

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        ip = get_client_ip(request)

        print("Latitude:", latitude)
        print("Longitude:", longitude)
        print("IP:", ip)

        return JsonResponse({
            "status": "ok",
            "latitude": latitude,
            "longitude": longitude,
            "ip": ip
        })

    return JsonResponse({"erro": "Método inválido"}, status=400)
