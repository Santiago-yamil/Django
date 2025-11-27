
from django.contrib import admin
from .models import Apoyo, Solicitud, Evaluador, Evaluacion, Notificacion

admin.site.register(Apoyo)
admin.site.register(Solicitud)
admin.site.register(Evaluador)
admin.site.register(Evaluacion)
admin.site.register(Notificacion)
# Register your models here.
