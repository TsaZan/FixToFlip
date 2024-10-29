from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView

from FixToFlip.accounts.models import BaseAccount
from FixToFlip.blog.forms import BlogPostForm
from FixToFlip.blog.models import BlogPost
from FixToFlip.dashboard.forms import PropertyAddForm, BlogPostDeleteForm, AddBlogPostForm
from FixToFlip.properties.models import Property


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard-index.html'


class DashboardPropertyView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/properties-list.html'


class DashboardTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/tasks.html'


class PropertyDetailsView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'dashboard/property-details.html'


class PropertyAddView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyAddForm
    template_name = 'dashboard/add-property.html'
    success_url = reverse_lazy('properties_main_page')


class ProfileEditTemplate(LoginRequiredMixin, TemplateView):
    model = BaseAccount
    template_name = 'dashboard/profile.html'
    success_url = reverse_lazy('dashboard')
    fields = '__all__'


class DashboardCreditsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/credits-list.html'


class DashboardExpensesView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/expenses-list.html'


class CreditAddView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyAddForm
    template_name = 'dashboard/add-credit.html'
    success_url = reverse_lazy('credits_main_page')


class BlogPostsView(LoginRequiredMixin, TemplateView):
    model = BlogPost
    template_name = 'dashboard/blogposts-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = BlogPost.objects.all()
        return context


class AddBlogPostView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = AddBlogPostForm
    template_name = 'dashboard/add-blogpost.html'
    success_url = reverse_lazy('dashboard_blogposts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditBlogPostView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = AddBlogPostForm
    template_name = 'dashboard/edit-blogpost.html'

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy('edit_blogpost', kwargs={'slug': slug})


class DeleteBlogPostView(PermissionRequiredMixin,LoginRequiredMixin, DeleteView):
    model = BlogPost
    form_class = BlogPostDeleteForm
    template_name = 'dashboard/delete-blogpost.html'
    success_url = reverse_lazy('dashboard_blogposts')
    permission_required = ('dashboard.delete_blogpost',)

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
