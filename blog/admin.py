from django.contrib import admin

from .models import Comment, Post


class ComPostInline(admin.StackedInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'img')
    list_filter = ('author',)
    ordering = ('title',)
    inlines = [
        ComPostInline,
    ]


@admin.action(description='Publish comment')
def pub_com(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.register(Comment)
class ComAdmin(admin.ModelAdmin):
    list_display = ('username', 'text', 'post', 'is_published')
    list_filter = ('username', 'post')
    ordering = ('is_published', 'post')
    actions = [pub_com]
