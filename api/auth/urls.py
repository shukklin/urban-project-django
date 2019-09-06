from django.conf.urls import url
from .views import SignUp
from rest_framework_simplejwt.views import (
   token_obtain_pair, token_refresh
)

urlpatterns = [
    url(r'^sign-in/$', token_obtain_pair, name='obtain-token'),
    url(r'^refresh/$', token_refresh, name='refresh-token'),
    url(r'^sign-up/$', SignUp.as_view(), name='sign-up'),
]
