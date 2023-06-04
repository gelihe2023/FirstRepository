from django.test import TestCase, Client
from django.db.models import Max
from .models import Airport, Flights, Pasajero

# Create your tests here. 

# Definimos un test de tipo TestCase (de Unittest aunque 
# se importe de Django)

class FlightTestCase(TestCase):
    
    def setUp(self): # Función especial de Django. Obligatorio

        # First we create several dummy values (for a Test DB created by Django)

        # Create airports in the Airport DB específico para el test
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights in the Flights DB, específico para el test

        Flights.objects.create(origin= a1, destination = a2, duration = 100)
        Flights.objects.create(origin= a1, destination = a1, duration = 200)
        Flights.objects.create(origin= a1, destination = a2, duration = -100)

        # Now we define the tests

    def test_departures_count(self): 
        # departures of an Airport Object
        # was a list of departures from that Airport
        a = Airport.objects.get(code="AAA") #Get the airport from Airports

        self.assertEqual(a.departures.count(),3) # Verify both numbers are equal.

    def test_arrivals_count(self):
        # arrivals of an Airport Object
        # was a list of arrivals from that Airport
        a = Airport.objects.get(code="AAA")

        self.assertEqual(a.arrivals.count(),1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flights.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue (f.is_valid_flight()) # Comprueba si f.is_valid_flight() es True

    def test_invalid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flights.objects.get(origin=a1, destination=a1)
        self.assertFalse (f.is_valid_flight()) # Comprueba si f.is_valid_flight() es False
        
    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flights.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse (f.is_valid_flight()) # Comprueba si f.is_valid_flight() es False

# Para ejecutar TESTS no hace falta ejecuter unittest.main()... se hace con:

#       python manage.py test

#

########################################
# Estos tests son para comprobar que la página funciona bien

    def test_index(self):
        # Client parece ser un objeto cliente de browser (capaz de 
        # descargar páginas)
        # Admite atributos como response/request al cargar una página)
        c = Client()
        response = c.get("/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["vuelos"].count(),3)

        # atributo "CONTEXT" se refiere a un diccionario con los valores
        # bajo "flights"

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flights.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)       

    def test_invalid_flight_page(self):
        max_id = Flights.objects.all().aggregate(Max("id"))["id__max"]
       

    #[id__max] entiende como el mayor id de la tabla                           

        c = Client()
        response = c.get(f"/flights/{max_id}") # Al buscar una página con 
        # idmax+1 debería fallar
        self.assertEqual(response.status_code, 404)  
        # Comprobar que da error de página (not found -404)

    def test_flight_page_passengers(self):

        f = Flights.objects.get(pk=1)

        p = Pasajero.objects.create(first="Alice", last="Adams")
        
        f.Pasajeros.add(p) #Añade el pasajero a un vuelo f

        c = Client()

        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pasajeros"].count(),1) 
        # Solo hemos creado un pasajero luego debería ser OK

    def test_flight_page_non_passengers(self):
                
        f = Flights.objects.get(pk=1) # primer vuelo
        p = Pasajero.objects.create(first="Alice", last="Adams")

        c = Client()

        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["no_aun"].count(),1) 
