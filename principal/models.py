# principal/models.py
# principal/models.py

from django.db import models
# ¡NECESITAS ESTA LÍNEA!
from django.core.validators import MinValueValidator, MaxValueValidator


# Tabla de Apoyos (La clave primaria id es VARCHAR)
class Apoyo(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    prerrequisitos = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'apoyos' # Ej. 'apoyos', 'solicitudes'

    def __str__(self):
        return self.nombre

# Tabla de Solicitudes (Relacionada a Apoyos)
class Solicitud(models.Model):
    # El id es SERIAL/int por defecto en Django, no es necesario declararlo
    curp = models.CharField(max_length=18, unique=True)
    nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    genero = models.CharField(max_length=20, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    ine_url = models.CharField(max_length=255, blank=True, null=True)
    cv_url = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=50, default='ENVIADA')
    
    # Clave Foránea: Relación con la tabla Apoyos
    apoyo = models.ForeignKey(
        Apoyo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        db_column='apoyo_id' # Mantiene el nombre de la columna en la BD
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'solicitudes'

    def __str__(self):
        return f"{self.nombre} {self.primer_apellido} ({self.curp})"

# Tabla de Evaluadores
class Evaluador(models.Model):
    # id SERIAL/int por defecto
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=150, unique=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'evaluadores'

    def __str__(self):
        return self.nombre

# Tabla de Evaluaciones (Relacionada a Solicitudes y Evaluadores)
class Evaluacion(models.Model):
    # Claves Foráneas
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, db_column='solicitud_id')
    evaluador = models.ForeignKey(Evaluador, on_delete=models.CASCADE, db_column='evaluador_id')
    
    # Campo de Calificación con restricción
    calificacion = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    comentarios = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'evaluaciones'


# Tabla de Notificaciones (Relacionada a Solicitudes)
class Notificacion(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, db_column='solicitud_id')
    mensaje = models.TextField()
    tipo = models.CharField(max_length=50, blank=True, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'notificaciones'