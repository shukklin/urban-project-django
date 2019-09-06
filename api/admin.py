from django.contrib import admin
from .models import Tree, Photo, Record, User, CommonName, ScientificName, SiteType

admin.site.register(Tree)
admin.site.register(Photo)
admin.site.register(Record)
admin.site.register(User)
admin.site.register(CommonName)
admin.site.register(ScientificName)
admin.site.register(SiteType)
