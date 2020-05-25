from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('^accounts/', include('allauth.urls')),
    path('accounts/profile/', include('users.urls', namespace='profiles')),
    path('', include('feed.urls', namespace='posts')),
    path('posts/', include('feed.urls', namespace='posts')),
    path('posts/', include('comments.urls', namespace='comments')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
