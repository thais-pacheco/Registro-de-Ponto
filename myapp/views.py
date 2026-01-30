from django.shortcuts import render
from django.utils import timezone

# Create your views here.
def mysite(request):
    hora_atual = timezone.now()
    return render(request, 'myapp/index.html', {'hora_atual': hora_atual})