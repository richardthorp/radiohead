from django.contrib import admin
from .models import (PortalImagesPost, PortalTextPost, PortalVideoPost,
                     TextPostComment, VideoPostComment, ImagesPostComment)


class PortalImagesPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PortalTextPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PortalVideoPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(PortalImagesPost, PortalImagesPostAdmin)
admin.site.register(PortalTextPost, PortalTextPostAdmin)
admin.site.register(PortalVideoPost, PortalVideoPostAdmin)
admin.site.register(TextPostComment)
admin.site.register(VideoPostComment)
admin.site.register(ImagesPostComment)
