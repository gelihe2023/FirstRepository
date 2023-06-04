from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="indexo"),
    path('<int:vol_id>', views.vuelo, name="vuelo"),
    path("<int:flight_id>/book", views.book, name="book"),
]