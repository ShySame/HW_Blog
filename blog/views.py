from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from practice.settings.components.email import EMAIL_HOST_USER

from .forms import CommentForm, HelpForm
from .models import Comment, Post

User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = "base_generic.html"


class PostView(generic.ListView):
    model = Post
    queryset = Post.objects.select_related("author").\
        filter(published=True).annotate(num=Count('comment'))
    paginate_by = 20


class AuthorView(generic.ListView):
    model = User
    template_name = 'blog/user_list.html'
    queryset = User.objects.annotate(num=Count('post'))
    paginate_by = 20


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        q = Comment.objects.filter(post_id=self.object.pk).filter(is_published=True)
        contex = super(PostDetailView, self).get_context_data()
        contex['com'] = q
        contex['form'] = CommentForm(initial={'post': self.object})
        return contex

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save()
        post = self.get_object()
        email = Post.objects.get(id=self.object.id).author.email
        # -----------just for me-------------------------------
        send_mail('New comment',
                  f"New comment on post: {post}. "
                  f"Was written by {comment.username}. "
                  f"URL:{reverse('blog:post_detail', kwargs={'pk': self.object.id})}",
                  EMAIL_HOST_USER, ['olyaluchko@gmail.com', ], fail_silently=True)
        # -----------------------------------------------------
        send_mail('New comment',
                  f"New comment on post: {post}. "
                  f"Was written by {comment.username}. "
                  f"URL:{reverse('blog:post_detail', kwargs={'pk': self.object.id})}",
                  'admin@mail.com', [email, ], fail_silently=True)

        Comment(username=comment.username,
                text=comment.text, is_published=False,
                post_id=post)
        return super(PostDetailView, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'text', 'img', 'description', 'author', 'published']

    def get_success_url(self):
        send_mail('New post', f"New post: {self.object.title}({self.object.pk})",
                  "admin@mail.com", ['admin@mail.com', ])
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'text', 'img', 'description', 'published']
    template_name = 'blog/post_update_form.html'

    def get_context_data(self, *args, **kwargs):
        queryset = Post.objects.get(id=self.kwargs['pk'])
        contex = super().get_context_data()
        contex['post_list'] = queryset
        return contex

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class UserPostView(generic.ListView):
    model = Post
    template_name = "blog/userpost.html"

    def get_context_data(self, *args, **kwargs):
        queryset = Post.objects.filter(author_id=self.kwargs['pk'])
        contex = super().get_context_data()
        contex['post_list'] = queryset
        contex['ifuser'] = True
        return contex


def contact_form(request):
    if request.method == "POST":
        form = HelpForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            send_mail(subject, message, from_email, ['admin@mail.com', ])
            # messages.add_message(request, messages.SUCCESS, 'Message sent')
            return redirect('blog:index')
    else:
        form = HelpForm()
    return render(
        request,
        "blog/help.html",
        context={
            "form": form,
        }
    )
