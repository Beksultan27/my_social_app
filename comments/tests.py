from django.test import TestCase
from .views import *
from .models import Comment
from feed.models import Post


class ModelTests(TestCase):

    def setUp(self):

        a1 = Post.objects.create(title='rawr', description='rserse', created_at='02.05.2020')
        b1 = Comment.objects.create(text='FIRST', post='SOME POST', owner='HOOMAN')

        Comment.objects.create()

