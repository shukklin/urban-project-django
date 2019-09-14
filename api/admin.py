from django.contrib import admin
from api.models import Object, Photo, User, ObjectType

admin.site.register(Object)
admin.site.register(Photo)
admin.site.register(User)
admin.site.register(ObjectType)