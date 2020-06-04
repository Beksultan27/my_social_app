from django.urls import path
from .views import PostListView, PostDetailView, PostUpdateView, PostDeleteView, PostLikeView, PostUnlikeView

app_name = 'feed'

urlpatterns = [
    path('', PostListView.as_view(), name='posts-list'),
    path('<int:id>/detail/', PostDetailView.as_view(), name='posts-detail'),
    path('<int:id>/update/', PostUpdateView.as_view(), name='posts-update'),
    path('<int:id>/delete/', PostDeleteView.as_view(), name='posts-delete'),
    path('<int:id>/like/', PostLikeView.as_view(), name='post-likes'),
    path('<int:id>/unlike/', PostUnlikeView.as_view(), name='post-unlikes'),
]
