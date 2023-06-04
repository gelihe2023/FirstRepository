from django.db import models

# Create your models here.

# En models.py definimos las tablas (tables) que se utilizarán y se registrarán en la DB
# Para ello:
#   1) Se definen tablas en models.py
#   2) Se ejecuta el comando "python manage.py makemigrations" This command creates some 
#      Python files that will create or edit our database to be able to store what we have
#      in our models.
#      Es decir, con este comando se crean los archivos .py que produciran con el siguiente
#      comando las TABLAS en la BASE de DATOS
#      ADEMAS: Crea la tabla db.sqlite3
#   3) Se ejecuta el comando "python manage.py migrate". Este comando ejecuta los archivos 
#      creando las tablas definidas en "models.py" en la BASE de DATOS (sqlite3)
#
#   2) y 3) Se deben ejecutar cada vez que cualquiera de los models cambie o se añada.
#
#   Los modelos (luego tablas) se definen como tablas y los campos como atributos (fields)
#   Por etiqueta, las clases son capitalizadas (primera letra mayúscula)
#
#   Clase del tipo models.Model
#   Se especifican los campos, primero en el ejemplo como models.Charfield () (string of char)
#   Pero luego se cambiarán esos campos por ForeignKeys (ya que se relacionarán varias tablas)

# Ahora creamos otro model (clase/tabla) para definir los aeropuertos (esta tabla sera
# referenciada luego por el modelo/clase/tabla "Flights".

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    # Aquí también definimos __str__(self) para poder presentar datos como string al 
    # llamar a la variable del objeto de la clase "Airport"

    def __str__(self):
        return f'{self.city} ({self.code})'
    ####################################################

  
class Flights(models.Model):
    # Al definir la clase Airports ahora podemos cruzar las tablas, haciendo que "origin/destination"
    # acudan a la tabla, es decir "origin" y "destination" cambian el TIPO a "models.ForeignKey"
            # origin = models.CharField(max_length=64)
            # destination = models.CharField (max_length=64)
    origin = models.ForeignKey(Airport, on_delete= models.CASCADE, related_name= "departures")
    destination = models.ForeignKey(Airport, on_delete= models.CASCADE, related_name= "arrivals")
    duration = models.IntegerField()

    ## IMPORTANTE: En ForeignKey usamos 3 atributos:
    #   1) Airport: indicamos una clase, diciendo que el origin/destination es una clase
    #   2) on_delete= models.CASCADE: indica que en caso que el objeto "Airport" desaparezca
    #   desaparecerán también todos los "Flights" asociados (método de Django). Hay otras opciones.
    #   3) related_name= "departures"/"arrivals". Hace una relación inversa... permite que dado 
    #   Un objeto Airport: se encuentren todos los objetos Flights relacionados (con ese Airport
    #   como salida: "departures" o como llegada:"arrivals")

    # if we print the class Flights then it will appear Flights object(1) only

    # To be able to read the values we will need to specifically define a 
    # method of how to do it: def __str__(self) como string.

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"
    
    ## MANY TO MANY RELATIONS ##

    # Aquí creamos la lista de "Pasajeros" que tendra una relación ManytoMany con los vuelos
    # Múltiples pasajeros para un vuelo y múltiples vuelos para un pasajero.
    # A la hora de definir el campo "vuelo" se definirá como "ManytoManyField" indicando eso.

#ERROR TEST PARTE DEL CURSO TEST
# Añadimos una función para comprobar que todo vaya bien

    def is_valid_flight(self):
        return self.origin != self.destination and self.duration > 0
     # El test que hacemos es comprobar si origen y destino son distintos y la duración > 0

# TESTS.PY se utilizará para programar tests para el projecto.


class Pasajero(models.Model):

    first = models.CharField (max_length=64)
    last = models.CharField (max_length=64)
    flight = models.ManyToManyField (Flights, blank=True, related_name= "Pasajeros")

    # Aquí:
      # 1) "first" y "last" seran texto: "models.CharField"
      # 2) los vuelos se definen con relación Many to Many pero:
      #       - Cada "flight" es un objeto "Flights" (con su origin, destination, duration)
      #       - blank=True, significa que se permite que no haya un vuelo registrado para pasajero
      #       - related_name, de nuevo permite hacer un listado de "Pasajeros" que tengan ese "flight"

      # También definimos un __str__(self):

    def __str__(self):
        return f'{self.first} {self.last}' 

    





