from django.urls import path

from .views import AuthJWT, GetToken

urlpatterns = [
    path('', AuthJWT.as_view(), name="jwt_auth"),
    path('getToken/', GetToken.as_view(), name="get_token"),
]
