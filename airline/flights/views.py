from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

# Lo primero es importar los models (clases/tablas) que usaremos

from .models import Flights, Airport, Pasajero

# Create your views here.

def index(request):
    return render(request,"flights/index.html",{
        "vuelos":Flights.objects.all()
    })

    # En index(request) se pasa como variable "vuelos" todos los objetos en Flights (all the fields)
    # Se pasa como variable a la página "index.html" en templates de la aplicación "flights"

def vuelo(request, vol_id):
    # Aquí actualizamos "vuelo" para que presente todos los "Pasajeros" del vuelo
    # Eso se logra aprovechando el "related_name= 'Pasajeros'" que definimos en "Models.Pasajero"
    flight = Flights.objects.get(id=vol_id)
    passangers = flight.Pasajeros.all() # Aquí se llama al metodo passangers.all de cada vuelo. 
    
    # Aquí creamos una lista con todos los pasajeros que NO estan en el vuelo, exclude(flight="flight")
    no_passangers = Pasajero.objects.exclude(flight=flight) 

    return render(request,"flights/vuelo.html",{
        "vol": flight,
        "pasajeros": passangers,
        "no_aun": no_passangers })

    #   Es decir, como parámetro recibimos "vol_id" (una cifra en el url)
    #   Se identifica el vuelo con ese vol_id con el comando Django: "Flights.objects.get(id=vol_id)"
    #   Y luego se pasa ese objeto (el vuelo con codigo vol_id) como parámetro para la HTML
    #   Además de la lista de pasajeros obtenida del vuelo, gracias al atributo "passangers"


    ###### BOOK A FLIGHT #########
    # Función para registrar BOOKINGS en cada vuelo

def book(request, flight_id):

    # Primero se comprueba si se han obtenido los datos por "POST", y luego se tratan los datos
    # recibidos por POST (del formulario de la página web del vuelo)

    if request.method == 'POST':

        # Primero se localiza (se obtiene-"get") el vuelo con sus datos

        vol = Flights.objects.get(id= flight_id)

        # Después del formulario se busca el ID del pasajero de los datos recibidos, 
        # que será un id (integer) como veremos en "vuelo.html"

        pasaj_id = int (request.POST['passante'])

        # De ese ID se obtinen todos los datos del model (clase/tabla) "Pasajero"

        pasajero = Pasajero.objects.get(id=pasaj_id)

        # Ahora registramos el vuelo en el perfil de ese pasajero

        pasajero.flight.add(vol)

        # Al final del proceso se vuelve a la página del VUELO (se refresca)

        return HttpResponseRedirect(reverse("vuelo", args=(flight_id,)))
    
    ## Now we update VUELO para incluir la lista de NO PASAJEROS



