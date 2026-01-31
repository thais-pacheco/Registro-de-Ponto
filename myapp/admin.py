from django.contrib import admin
from .models import Registro

class RegistroAdmin(admin.ModelAdmin):
    list_display = ('dt_hora', 'latitude', 'longitude', 'ip', 'foto')
    search_fields = ('ip',)
    list_filter = ('dt_hora', 'ip')

admin.site.register(Registro, RegistroAdmin)
