from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('^accounts/', include('allauth.urls')),
    path('accounts/profile/', include('users.urls', namespace='profiles')),
    path('', Home.as_view(), name='home'),
]

# if settings.DEBUG:
#     from django.conf.urls.static import static
#
#     urlpatterns += static(
#         settings.STATIC_URL,
#         document_root=settings.STATIC_ROOT
#     )
#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )
