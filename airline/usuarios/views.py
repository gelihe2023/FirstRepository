from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

# En la página index (función index también) se presenta la primera página.
# Si el usuario NO está autentificado irá a la página de login.

def index(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")  
    
    #Como vimos para reenviar a una página usamos el método HttpResponseRedirect: que 
    # redirecciona a una página, y esa página se obtiene de hacer un "reverse" method
    # búsqueda del origen, a partir de la referencia definida en "urls", aquí "login"

# Ahora creamos la función "LoginRequest"

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("indexo"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid Credentials"
            })
    


    return render(request, "users/login.html")
# login_view nos lleva a la página login.html

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged Out."
    })

