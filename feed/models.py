from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse


class PostManager(models.Manager):
    def get_posts(self, *args, **kwargs):
        return self.all()

    def get_post(self, post_id, *args, **kwargs):
        return get_object_or_404(self, id=post_id)

    def get_user_posts(self, owner, *args, **kwargs):
        return self.filter(owner=owner)

    def get_user_post(self, post_id, user, *args, **kwargs):
        return get_object_or_404(self, pk=post_id, owner=user)


class LikeManager(models.Manager):
    def find_is_liked(self, post, user):
        return self.filter(post=post, owner=user)

    def create_like(self, post, user):
        like = self.create(post=post, owner=user)
        like.save()


class UnlikeManager(models.Manager):
    def find_is_unliked(self, post, user):
        return self.filter(post=post, owner=user)

    def create_unlike(self, post, user):
        unlike = self.create(post=post, owner=user)
        unlike.save()


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE, null=True)

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


class Like(models.Model):
    post = models.ForeignKey(Post, default=1, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    objects = LikeManager()

    def __str__(self, *args, **kwargs):
        return self.post.title

    def get_like_url(self, *args, **kwargs):
        return reverse('likes:post-likes', kwargs={'id': self.pk})


class Unlike(models.Model):
    post = models.ForeignKey(Post, default=1, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    objects = UnlikeManager()

    def __str__(self, *args, **kwargs):
        return self.post.title

    def get_unlike_url(self, *args, **kwargs):
        return reverse('unlikes:post-unlikes', kwargs={'id': self.pk})

