from allauth.account.forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from FixToFlip.accounts.forms import ProfileEditForm, UserEditForm, UserDeleteForm
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
    model = BaseAccount
    fields = '__all__'
    profile_edit_form = ProfileEditForm
    user_edit_form = UserEditForm
    template_name = 'dashboard/profile.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        if self.request.POST:
            context['user_form'] = UserEditForm(self.request.POST, instance=user)
            context['profile_form'] = ProfileEditForm(self.request.POST, instance=user.profile)
        else:
            context['user_form'] = UserEditForm(instance=user)
            context['profile_form'] = ProfileEditForm(instance=user.profile)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserEditForm(request.POST, instance=self.object)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=self.object.profile)

        if user_form.is_valid() and profile_form.is_valid():
            if 'delete_picture' in request.POST and request.POST['delete_picture'] == 'on':
                self.object.profile.profile_picture = None
                self.object.profile.save()

            user_form.save()
            profile_form.save()
            return redirect(self.success_url())
        else:
            return self.render_to_response(self.get_context_data(user_form=user_form, profile_form=profile_form))

    def success_url(self):
        return reverse_lazy('profile_edit', kwargs={'pk': self.object.pk})


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BaseAccount
    template_name = 'dashboard/delete-account.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user
