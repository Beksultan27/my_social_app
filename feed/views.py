from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView, UpdateView, DeleteView, CreateView
from PIL import Image
from django.core.files.base import ContentFile

from .models import Post, Like, Unlike
from .forms import PostModelForm


class PostListView(CreateView):
    model = Post
    form = PostModelForm
    template_name = 'post_list.html'
    context = {}

    def get(self, request, *args, **kwargs):
        qs = self.model.objects.get_posts()
        form = self.form()
        self.context['title'] = 'Posts'
        self.context['posts'] = qs
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = self.request.user
            instance.save()
            messages.success(request, 'Post has been added to feed!')
            return redirect('posts:posts-list')
        messages.error(request, 'Oop! Enter valid details!')
        return reverse('posts:posts-list')


class PostDetailView(DetailView):
    queryset = Post.objects.all()
    context_object_name = 'post'
    lookup = 'id'
    template_name = 'post_detail.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs.get(self.lookup))

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Post Detail'
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    queryset = Post.objects.all()
    form_class = PostModelForm
    context_object_name = 'post'
    template_name = 'post_update.html'
    lookup = 'id'

    def get_object(self, *args, **kwargs):
        return Post.objects.get_user_post(
            self.kwargs.get(self.lookup),
            self.request.user
        )

    def get_context_data(self, *args, **kwargs):
        context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Post Update'
        return context

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Post has been updated successfully!')
        return reverse('posts:posts-detail', kwargs={'id': self.kwargs.get(self.lookup)})

    def image_update(self, request, pk, template_name):
        post = get_object_or_404(Post, pk=pk)
        form = self.form_class(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.save()
            return redirect('posts:posts-detail')
        return render(request, template_name, {'form': form})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    queryset = Post.objects.all()
    context_object_name = 'post'
    template_name = 'post_delete.html'
    lookup = 'id'

    def get_object(self, *args, **kwargs):
        return Post.objects.get_user_post(
            self.kwargs.get(self.lookup),
            self.request.user
        )

    def get_context_data(self, *args, **kwargs):
        context = super(PostDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Post Delete'
        return context

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Post has been deleted!')
        return reverse('posts:posts-list')


class PostLikeView(LoginRequiredMixin, View):
    lookup = 'id'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs.get(self.lookup))

    def get(self, request, id=None, *args, **kwargs):
        is_liked = Like.objects.find_is_liked(self.get_object(), request.user)

        if is_liked.exists():
            messages.error(request, 'Post has already been liked!')
            return redirect(reverse('posts:posts-list'))
        else:
            is_unliked = Unlike.objects.find_is_unliked(self.get_object(), request.user)

            if is_unliked.exists():
                is_unliked.delete()
                Like.objects.create_like(self.get_object(), request.user)
                messages.success(request, 'Post has been liked!')
                return redirect(reverse('posts:posts-list'))
            else:
                Like.objects.create_like(self.get_object(), request.user)
                messages.success(request, 'Post has been liked!')
                return redirect(reverse('posts:posts-list'))


class PostUnlikeView(LoginRequiredMixin, View):
    lookup = 'id'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs.get(self.lookup))

    def get(self, request, id=None, *args, **kwargs):
        is_unliked = Unlike.objects.find_is_unliked(self.get_object(), request.user)

        if is_unliked.exists():
            messages.error(request, 'Post has already been unliked!')
            return redirect(reverse('posts:posts-list'))
        else:
            is_liked = Like.objects.find_is_liked(self.get_object(), request.user)
            if is_liked.exists():
                is_liked.delete()
                Unlike.objects.create_unlike(self.get_object(), request.user)
                messages.success(request, 'Post has been unliked!')
                return redirect(reverse('posts:posts-list'))
            else:
                Unlike.objects.create_unlike(self.get_object(), request.user)
                messages.success(request, 'Post has been unliked!')
                return redirect(reverse('posts:posts-list'))
