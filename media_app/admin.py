from django.contrib import admin
from .models import Single, Comment


class SingleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Single, SingleAdmin)
admin.site.register(Comment)
