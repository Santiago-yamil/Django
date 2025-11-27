from django.shortcuts import render
from rest_framework import viewsets
from .models import Apoyo, Solicitud, Evaluador, Evaluacion, Notificacion
from .serializers import (
    ApoyoSerializer, SolicitudSerializer,
    EvaluadorSerializer, EvaluacionSerializer,
    NotificacionSerializer
)

from .permissions import IsSolicitante, IsEvaluador

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status





class ApoyoViewSet(viewsets.ModelViewSet):
    queryset = Apoyo.objects.all()
    serializer_class = ApoyoSerializer

#class SolicitudViewSet(viewsets.ModelViewSet):
    #queryset = Solicitud.objects.all()
    #serializer_class = SolicitudSerializer

class EvaluadorViewSet(viewsets.ModelViewSet):
    queryset = Evaluador.objects.all()
    serializer_class = EvaluadorSerializer

#class EvaluacionViewSet(viewsets.ModelViewSet):
 #   queryset = Evaluacion.objects.all()
  #  serializer_class = EvaluacionSerializer

class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer

#class SolicitudViewSet(viewsets.ModelViewSet):
#    queryset = Solicitud.objects.all()
#    serializer_class = SolicitudSerializer
#    permission_classes = [IsSolicitante]  # solo solicitantes
#
#    def get_queryset(self):
#        # cada solicitante solo ve sus solicitudes
#        return Solicitud.objects.filter(usuario=self.request.user)


class EvaluacionViewSet(viewsets.ModelViewSet):
    queryset = Evaluacion.objects.all()
    serializer_class = EvaluacionSerializer
    permission_classes = [IsEvaluador]  # solo evaluadores


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    @action(detail=True, methods=['post'])
    def enviar(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.estado == 'EN_CAPTURA':
            solicitud.estado = 'ENVIADA'
            solicitud.save()
            return Response({'status': 'Solicitud enviada'})
        return Response({'error': 'No se puede enviar'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def seleccion_final(request):
    seleccionados = request.data.get("seleccionados", [])
    for item in seleccionados:
        curp = item.get("curp")
        score = item.get("score")
        try:
            solicitud = Solicitud.objects.get(curp=curp)
            solicitud.estado = "SELECCIONADA"
            # si tienes campo score_final, lo guardas:
            if hasattr(solicitud, "score_final"):
                solicitud.score_final = score
            solicitud.save()
        except Solicitud.DoesNotExist:
            continue

    return Response({"status": "Selección final guardada ✅"}, status=status.HTTP_200_OK)
