from django.contrib import admin
from .models import Flights, Airport, Pasajero

# Para poder administrar facilmente Django tiene el modo ADMIN
# Desde aquí se pueden administrar tablas y bases de dato de la aplicación
# Se crea usario con: "python manage.py createsuperuser"
# Después se configura este "admin.py", uno por aplicación/DB

# Se tienen que registrar los "models/clases/tablas"

# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    list_display = ("id","origin", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flight",)


admin.site.register(Flights, FlightAdmin)
admin.site.register(Airport)
admin.site.register(Pasajero, PassengerAdmin)

# Para acceder al admin, lo que hay que hacer es incluir admin en el browser: .../flights/admin
