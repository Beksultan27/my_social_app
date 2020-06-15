from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from actions.utils import create_action
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity

from .models import Post
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


@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
                create_action(request.user, 'likes', post)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})


@login_required
def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'list_ajax.html',
                      {'section': 'posts', 'posts': posts})
    return render(request,
                  'list.html',
                  {'section': 'posts', 'posts': posts})


def post_search(request):
    query = request.POST.get('search_form')
    results = []
    if query:
        results = Post.objects.annotate(similarity=TrigramSimilarity('title', query)). \
            filter(similarity__gt=0.05).order_by('-similarity')
    return render(request, 'post_search.html', {'query': query, 'results': results})
