from django.contrib import admin
from mainsite.models import User, BlogPost, BlogComment, Category


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
