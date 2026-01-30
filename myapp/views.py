from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import json
import uuid
import os
from django.conf import settings


def mysite(request):
    hora = timezone.localtime(timezone.now())
    return render(request, 'myapp/index.html', {'hora_atual': hora})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')



@csrf_exempt
def bater_ponto(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método inválido"}, status=405)

    latitude = request.POST.get("latitude")
    longitude = request.POST.get("longitude")
    foto = request.FILES.get("foto")

    if not foto:
        return JsonResponse({"erro": "Foto não enviada"}, status=400)

    hora = timezone.localtime()

    nome_arquivo = f"{uuid.uuid4()}.png"
    pasta = os.path.join(settings.MEDIA_ROOT)

    os.makedirs(pasta, exist_ok=True)

    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "wb") as f:
        for chunk in foto.chunks():
            f.write(chunk)

    print("PONTO REGISTRADO")
    print("Hora:", hora)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("IP:", request.META.get("REMOTE_ADDR"))
    print("Foto:", nome_arquivo)

    return JsonResponse({
        "status": "ok",
        "hora": hora.strftime("%d/%m/%Y %H:%M:%S"),
        "latitude": latitude,
        "longitude": longitude,
        "foto": nome_arquivo
    })

    return JsonResponse({"erro": "Método inválido"}, status=400)
