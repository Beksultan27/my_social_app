from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
import redis
from django.contrib.contenttypes.models import ContentType

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


class PostManager(models.Manager):
    def get_posts(self, *args, **kwargs):
        return self.all()

    def get_post(self, post_id, *args, **kwargs):
        return get_object_or_404(self, id=post_id)

    def get_user_posts(self, owner, *args, **kwargs):
        return self.filter(owner=owner)

    def get_user_post(self, post_id, user, *args, **kwargs):
        return get_object_or_404(self, pk=post_id, owner=user)


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE, null=True)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self, *args, **kwargs):
        return self.title

    def get_absolute_url(self, *args, **kwargs):
        return reverse('posts:posts-detail', kwargs={'id': self.pk})

    def get_delete_url(self, *args, **kwargs):
        return reverse('posts:posts-delete', kwargs={'id': self.pk})

    def get_update_url(self, *args, **kwargs):
        return reverse('posts:posts-update', kwargs={'id': self.pk})

    def get_comment_create_url(self, *args, **kwargs):
        return reverse('comments:comments-create', kwargs={'id': self.pk})

    @property
    def post_total_views(self):
        post = get_object_or_404(Post, id=self.id)
        total_views = r.incr('post:{}:views'.format(post.id))
        return total_views

