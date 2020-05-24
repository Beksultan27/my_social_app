from django.urls import path, include
# from django.contrib.auth import views as auth_views
from .views import (
    ProfileListView,
    ProfileDetailView,
    ProfileUpdateView,
    ProfileDeleteView,
)

app_name = 'users'

urlpatterns = [
    path('', ProfileListView.as_view(), name='profiles-list'),
    # path('create/', ProfileCreateView.as_view(), name='profiles-create'),
    path('<int:id>/detail/', ProfileDetailView.as_view(), name='profiles-detail'),
    path('<int:id>/delete/', ProfileDeleteView.as_view(), name='profiles-delete'),
    path('<int:id>/update/', ProfileUpdateView.as_view(), name='profiles-update'),
]
