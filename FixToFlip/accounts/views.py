from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from FixToFlip.accounts.forms import ProfileEditForm, UserEditForm, UserDeleteForm
from FixToFlip.accounts.models import BaseAccount


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = BaseAccount
    fields = '__all__'
    profile_edit_form = ProfileEditForm
    user_edit_form = UserEditForm
    template_name = 'dashboard/profile.html'

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
        profile_form = ProfileEditForm(request.POST, instance=self.object.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.success_url())
        else:
            return self.render_to_response(self.get_context_data(user_form=user_form, profile_form=profile_form))

    def success_url(self):
        return reverse_lazy('profile_edit', kwargs={'pk': self.object.pk})


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = BaseAccount
    template_name = 'dashboard/delete-account.html'
    success_url = reverse_lazy('index')

