from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

# from practice.settings.components.email import EMAIL_HOST_USER

from .forms import CommentForm, HelpForm
from .models import Comment, Post
from .tasks import need_send_mail

User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = "base_generic.html"


class PostView(generic.ListView):
    model = Post
    queryset = Post.objects.select_related("author"). \
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
        # send_mail('New comment',
        #           f"New comment on post: {post}. "
        #           f"Was written by {comment.username}. "
        #           f"URL:{reverse('blog:post_detail', kwargs={'pk': self.object.id})}",
        #           EMAIL_HOST_USER, ['olyaluchko@gmail.com', ], fail_silently=True)
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


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'text', 'img', 'description', 'published']
    template_name = 'blog/post_update_form.html'
    success_message = "Post updated"

    def get_context_data(self, *args, **kwargs):
        queryset = Post.objects.get(id=self.kwargs['pk'])
        contex = super().get_context_data()
        contex['post_list'] = queryset
        return contex


class UserPostView(generic.ListView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        queryset = Post.objects.filter(author_id=self.kwargs['pk']). \
            annotate(num=Count('comment')).order_by('pk')
        contex = super().get_context_data()
        contex['post_list'] = queryset
        contex['ifuser'] = True
        return contex


class AuthorPostView(generic.ListView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        queryset = Post.objects.filter(author_id=self.kwargs['pk']). \
            annotate(num=Count('comment')).order_by('pk')
        contex = super().get_context_data()
        contex['post_list'] = queryset
        return contex


def contact_form_save(request, form, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            data['form_is_valid'] = True
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            need_send_mail.apply_async((subject, from_email, message))
            messages.success(request, 'Email was send successfully')
            context = {'form': form}
            data['html_form'] = render_to_string(template_name, context, request=request)
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            messages.error(request, 'Email was not send')
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def contact_form(request):
    if request.method == "POST":
        form = HelpForm(request.POST)
    else:
        form = HelpForm()
    return contact_form_save(request, form, 'blog/help.html')
