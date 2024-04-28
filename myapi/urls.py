from django.urls import path

from . import views

app_name = "myapi"
urlpatterns = [
    path("hello-world/", views.hello_world, name="hello_world"),
    path("upload_tricks/", views.upload_run, name="upload_tricks"),
    path(
        "trick_definitions/",
        views.TrickDefinitionList.as_view(),
        name="trick_definitions",
    ),
    path("runs/", views.RunList.as_view(), name="runs"),
]
