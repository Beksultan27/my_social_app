from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from actions.utils import create_action
from actions.models import Contact
from .forms import *


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'account/signup.html'
    success_url = '/dev/accounts/login'

    def form_valid(self, form):
        messages.success(self.request, 'User has been registered successfully!')
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


class LoginView(View):
    form = LoginForm
    template_name = 'account/login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        form = self.form()
        self.context['title'] = 'Login'
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user_obj')
            login(request, user)
            messages.success(request, 'Yay! You just logged in!')
            return redirect(reverse('pages:dashboard-view'))
        self.context['title'] = 'Login'
        self.context['form'] = form
        return render(request, self.template_name, self.context)


class LogoutView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You has been logged out successfully!')
        return redirect(reverse('accounts:accounts-login'))


class ProfileObjectMixin(object):
    model = Profile
    lookup = 'id'

    def get_object(self, *args, **kwargs):
        return self.model.objects.get_auth_profile(
            self.kwargs.get(self.lookup),
            self.request.user
        )


class CheckAuthProfileMixin(object):
    model = Profile

    def get_object(self, *args, **kwargs):
        obj = self.model.objects.check_auth_profile(self.request.user)
        if not obj is None:
            return obj
        else:
            return None


class ProfileListView(ListView):
    queryset = Profile.objects.all()
    context_object_name = 'profiles'
    template_name = 'profiles/profiles_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Profiles'
        return context


class ProfileDetailView(DetailView):
    queryset = Profile.objects.all()
    context_object_name = 'profile'
    template_name = 'profiles/profile_detail.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Profile, pk=self.kwargs.get('id'))

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = self.get_object().name
        return context


class ProfileUpdateView(LoginRequiredMixin, ProfileObjectMixin, UpdateView):
    queryset = Profile.objects.all()
    context_object_name = 'profile'
    template_name = 'profiles/profile_update.html'
    form_class = ProfileForm

    def get_context_data(self, *args, **kwargs):
        if self.get_object():
            context = super(ProfileUpdateView, self).get_context_data(*args, **kwargs)
            context['title'] = 'Update Profile'
            return context

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Profile has been updated successfully!')
        return reverse(
            'profiles:profiles-detail', kwargs={'id': self.get_object().pk}
        )


class ProfileDeleteView(LoginRequiredMixin, ProfileObjectMixin, DeleteView):
    queryset = Profile.objects.all()
    context_object_name = 'profile'
    template_name = 'profiles/profile_delete.html'

    def get_context_data(self, *args, **kwargs):
        if self.get_object():
            context = super(ProfileDeleteView, self).get_context_data(*args, **kwargs)
            context['title'] = 'Delete Profile'
            return context

    def get_success_url(self, *args, **kwargs):
        messages.success(self.request, 'Profile has been deleted successfully!')
        return reverse('profiles:profiles-list')


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})
