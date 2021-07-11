from django.contrib import admin
from .models import Ad, Comment

class AdAdmin(admin.ModelAdmin):
    exclude = ['picture','content_type']

admin.site.register(Ad, AdAdmin)
admin.site.register(Comment)