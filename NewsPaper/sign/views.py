
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import BaseRegisterForm
from newsportal.models import Author


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/personal.html'

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

    """
    def form_valid(self, form):
        user = form.save(commit=False)
        try:
            return super().form_valid(form)
        finally:
            basic_group = Group.objects.get(name='common')
            basic_group.user_set.add(user)
    """

@login_required
def set_user_group_to_common(request):
    user = request.user
    common_group = Group.objects.get(name='common')
    if not request.user.groups.filter(name='common').exists():
        common_group.user_set.add(user)
    return redirect('/account/')


@login_required
def set_user_group_author(request):
    user_cur = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user_cur)
    Author.objects.create(user=user_cur)
    return redirect('/account/')