from django.contrib import admin
from .models import (PortalImagesPost, PortalTextPost, PortalVideoPost,
                     TextPostComment, VideoPostComment, ImagesPostComment)

admin.site.register(PortalImagesPost)
admin.site.register(PortalTextPost)
admin.site.register(PortalVideoPost)
admin.site.register(TextPostComment)
admin.site.register(VideoPostComment)
admin.site.register(ImagesPostComment)
