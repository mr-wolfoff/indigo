from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, BaseValidator

from multiupload.fields import MultiFileField

from webapp.models import Article, Picture, Video


def max_len_validator(string):
    if len(string) > 20:
        raise ValidationError('Заголовок должен быть длиннее 2 символов')
    return string


class CustomLenValidator(BaseValidator):
    def __init__(self, limit_value=100):
        message = 'Максимальная длина заголовка %(limit_value)s. Вы ввели %(show_value)s символов'
        super().__init__(limit_value=limit_value, message=message)

    def compare(self, value, limit_value):
        return value > limit_value

    def clean(self, value):
        return len(value)


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        validators=(MinLengthValidator(limit_value=2, message='message'), CustomLenValidator()))

    class Meta:
        model = Article
        fields = ('title', 'text', 'status', 'tags')
        labels = {
            'title': 'Заголовок статьи',
            'text': 'Текст',
            'status': 'Статус',
            'tags': 'Теги'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise ValidationError('Заголовок должен быть длиннее 2 символов')
        if Article.objects.filter(title=title).exists():
            raise ValidationError('Заголовок с таким именем уже есть')
        return title


class PictureForm(forms.ModelForm):
    source = MultiFileField(min_num=0, max_num=10)

    class Meta:
        model = Picture
        fields = ('source',)

    def save(self, commit=True):
        print(11111111111)
        instance = self.cleaned_data
        images = self.cleaned_data.get('source')
        if images:
            for image in images:
                picture = Picture(article=instance, source=image)
                if commit:
                    picture.save()
        return instance


class VideoForm(forms.ModelForm):
    source = MultiFileField(min_num=0, max_num=10)

    class Meta:
        model = Video
        fields = ('source',)

    def save(self, commit=True):
        instance = super().save(commit=False)
        videos = self.cleaned_data.get('source')
        if videos:
            for video in videos:
                video = Video(article=instance, source=video)
                if commit:
                    video.save()
        return instance


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label='Найти')


class FavoriteForm(forms.Form):
    note = forms.CharField(max_length=30, required=True, label='Заметка')
