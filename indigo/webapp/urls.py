from django.urls import path

from webapp.views.articles import ArticleDetail, ArticleUpdateView, \
    ArticleCreateView, ArticleDeleteView, FavoriteView
from webapp.views.base import IndexView, IndexRedirectView