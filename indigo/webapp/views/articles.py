from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView

from webapp.forms import ArticleForm, FavoriteForm, PictureForm, VideoForm
from webapp.models import Article, Video, Picture, Favorite, Tag


class ArticleCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'articles/article_create.html'
    model = Article
    form_class = ArticleForm
    success_message = 'Статья создана'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture_form'] = PictureForm()
        context['video_form'] = VideoForm()
        return context

    def form_valid(self, form):
        article = form.save()
        picture_form = PictureForm(self.request.POST, self.request.FILES)
        video_form = VideoForm(self.request.POST, self.request.FILES)

        if picture_form.is_valid():
            picture = picture_form.save(commit=False)
            picture.article = article
            picture.save()

        if video_form.is_valid():
            video = video_form.save(commit=False)
            video.article = article
            video.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.pk})


class ArticleDetail(DetailView):
    template_name = 'article.html'
    model = Article


class GroupPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['admin', 'manager']).exists()


class ArticleUpdateView(GroupPermissionMixin, LoginRequiredMixin, UpdateView):
    template_name = 'article_update.html'
    form_class = ArticleForm
    model = Article
    success_message = 'Статья обновлена'

    def get_success_url(self):
        return reverse('article_detail', kwargs={'pk': self.object.pk})


class ArticleDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'article_confirm_delete.html'
    model = Article
    success_url = reverse_lazy('index')
    success_message = 'Статья удалена'


class FavoriteView(LoginRequiredMixin, FormView):
    form_class = FavoriteForm

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            note = form.cleaned_data.get('note')
            user = request.user
            if not Favorite.objects.filter(user=user, article=article).exists():
                Favorite.objects.create(user=user, article=article, note=note)
                messages.success(request, 'Статья была добавлена в избранное')
        return redirect('index')
