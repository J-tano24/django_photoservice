from django.forms import ModelForm
from .models import Photo

# Photoを投稿する用のModelForm(モデルに紐づいたフォームであることを定義)を作製する。
class PhotoForm(ModelForm):
  class Meta:
    # そのモデルは、Photoモデルです。
    model = Photo
    fields = ['title', 'comment', 'image', 'category']