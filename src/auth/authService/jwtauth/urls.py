from django.urls import path

from .views import AuthJWT

urlpatterns = [
    path('', AuthJWT.as_view(), name="jwt_auth"),
]
