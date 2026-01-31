from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Registro
import uuid
import os


def mysite(request):
    hora = timezone.localtime()

    if 5 <= hora.hour < 12:
        mensagem = "Bom dia!"
    elif 12 <= hora.hour < 18:
        mensagem = "Boa tarde!"
    else:
        mensagem = "Boa noite!"

    return render(request, 'myapp/index.html', {
        'hora_atual': hora,
        'mensagem': mensagem
    })


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

    if not latitude or not longitude:
        return JsonResponse({
            "status": "erro",
            "mensagem": "Localização não detectada. Ative o GPS."
        }, status=400)

    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return JsonResponse({
            "status": "erro",
            "mensagem": "Latitude ou longitude inválida."
        }, status=400)

    if not foto:
        return JsonResponse({
            "status": "erro",
            "mensagem": "Foto não enviada."
        }, status=400)

    hora = timezone.localtime()

    if 5 <= hora.hour < 12:
        mensagem = "Bom dia!"
    elif 12 <= hora.hour < 18:
        mensagem = "Boa tarde!"
    else:
        mensagem = "Boa noite!"

    ip = get_client_ip(request)

    nome_arquivo = f"{uuid.uuid4()}.png"
    pasta = os.path.join(settings.MEDIA_ROOT, "fotos")
    os.makedirs(pasta, exist_ok=True)

    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "wb") as f:
        for chunk in foto.chunks():
            f.write(chunk)

    Registro.objects.create(
        dt_hora=hora,
        latitude=latitude,
        longitude=longitude,
        ip=ip,
        foto=f"fotos/{nome_arquivo}"
    )

    return JsonResponse({
        "status": "ok",
        "mensagem": mensagem,
        "hora": hora.strftime("%d/%m/%Y %H:%M:%S"),
        "latitude": latitude,
        "longitude": longitude,
        "foto": nome_arquivo
    })
