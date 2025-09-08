from django.urls import path
from . import views

urlpatterns = [
    path ('insert-department/', views.insert_department),
    path ('get-department/', views.get_department)
]