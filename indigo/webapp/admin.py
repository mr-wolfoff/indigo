from django.contrib import admin

from webapp.models import Article, Picture, Video


class PictureInline(admin.StackedInline):
    model = Picture
    fields = ('source',)
    extra = 0

class VideoInline(admin.StackedInline):
    model = Video
    fields = ('source',)
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    inlines = [PictureInline, VideoInline]
    list_display = ('id', 'title', 'author', 'created_at')
    list_filter = ('id', 'title', 'author', 'created_at')
    search_fields = ('title', 'author')
    fields = ('text', 'title', 'created_at')
    readonly_fields = ('id', 'created_at', 'author', 'updated_at')


admin.site.register(Article, ArticleAdmin)
