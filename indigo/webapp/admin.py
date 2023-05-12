from django.contrib import admin

from webapp.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    list_filter = ('id', 'title', 'author', 'created_at')
    search_fields = ('title', 'author')
    fields = ('text', 'title', 'author', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')


admin.site.register(Article, ArticleAdmin)
