from django.conf.urls import url, include

urlpatterns = [
    url(r'^auth/', include('api.auth.urls'), name='auth'),
    url(r'^table/', include('api.table.urls'), name='table'),
]
