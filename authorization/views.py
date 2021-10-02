from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from authorization.forms import RegisterForm

User = get_user_model()


class RegisterFormView(generic.CreateView):
    template_name = 'registration/registr.html'
    form_class = RegisterForm

    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        form.cleaned_data.get("password1")

        user = authenticate(username=user.username, password=user._password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = 'registration/user_edit.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'registration/user.html'
