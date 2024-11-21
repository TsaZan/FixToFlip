from allauth.account.forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from FixToFlip.accounts.forms import ProfileEditForm, UserEditForm
from FixToFlip.accounts.models import BaseAccount, Profile


def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False}, status=400)


def ajax_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return JsonResponse({'success': True, 'refresh': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'dashboard/profile.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = user.profile
        return {
            'user_form': UserEditForm(instance=user),
            'profile_form': ProfileEditForm(instance=profile),
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile

        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_edit', pk=self.kwargs['pk'])

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BaseAccount
    template_name = 'dashboard/delete-account.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user
