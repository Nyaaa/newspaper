from django.contrib import admin
from .models import Post, Comment, Category, Author
from modeltranslation.admin import TranslationAdmin


# Register your models here.
class PostAdmin(TranslationAdmin):
    model = Post
    list_display = ('title', 'author', 'created', 'type')
    list_filter = ('author', 'type')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'post', 'created', 'user')


def update_rating(modeladmin, request, queryset):
    for author in queryset:
        author.update_rating()


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'rating')
    actions = [update_rating]

    def name(self, obj):
        return obj.user.get_full_name()


class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
