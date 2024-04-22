from django.urls import path, include
from .views import loginView, registerView, CookieTokenRefreshView, logoutView, user


app_name = "authentication"

urlpatterns = [
    path('login', loginView, name='login_url'),
    path('register', registerView, name='register'),
    path('refresh-token', CookieTokenRefreshView.as_view()),
    path('logout', logoutView),
    path("user", user),
]
