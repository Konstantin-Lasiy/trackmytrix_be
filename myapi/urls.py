from django.urls import path
from . import views

app_name='myapi'
urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path('weight-entries/', views.weight_entries, name='weight_entries'),
    path('weight-entry/<int:pk>/', views.weight_entry_detail, name='weight_entry_detail'),
]