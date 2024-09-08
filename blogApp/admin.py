from django.contrib import admin
from .models import Article,Comment,Category
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
