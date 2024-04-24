from django.urls import path
from . import views

app_name = "myapi"
urlpatterns = [
    path("hello-world/", views.hello_world, name="hello_world"),
    path("upload_tricks/", views.upload_run, name="upload_tricks"),
    path("trick_definitions/", views.get_trick_definitions, name="trick_definitions"),
]
