from django.urls import path
from .views import PostListView, PostDetailView, PostUpdateView, PostDeleteView
from feed import views

app_name = 'feed'

urlpatterns = [
    path('', PostListView.as_view(), name='posts-list'),
    path('<int:id>/detail/', PostDetailView.as_view(), name='posts-detail'),
    path('<int:id>/update/', PostUpdateView.as_view(), name='posts-update'),
    path('<int:id>/delete/', PostDeleteView.as_view(), name='posts-delete'),
    path('like/', views.post_like, name='like'),
    path('', views.post_list, name='list'),
    path('search/', views.post_search, name='post_search'),
]

