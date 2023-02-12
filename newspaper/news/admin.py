from django.contrib import admin
from .models import Post, Comment, Category, Author


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'type')
    list_filter = ('author', 'type')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'post', 'created', 'user')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'rating')

    def name(self, obj):
        return obj.user.get_full_name()


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
