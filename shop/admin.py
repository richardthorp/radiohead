from django.contrib import admin
from .models import Album, Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Album, AlbumAdmin)
admin.site.register(Product, ProductAdmin)
