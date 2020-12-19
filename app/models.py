from django.db import models
# UserモデルはDjangoにデフォルトで入っているモデルになるので、インポートすれば、userやemail等のプロパティを使用できる。
from django.contrib.auth.models import User

# Create your models here.

# Categoryというモデルは存在しない為、作成してやらないといけない。
class Category(models.Model):
  title = models.CharField(max_length=20)

  def __str__(self):
    return self.title

class Photo(models.Model):
  title = models.CharField(max_length=150)
  comment = models.TextField(blank=True)
  # アップロード先をphotosに指定しており、imageフィールドからアップされた画像は、プロジェクト/media/photosの中に保存される。
  image = models.ImageField(upload_to='photos')
  # Categoryモデルを使えるようにし、categoryフィールドを作っている。マイグレーションファイルを作るときは、default値を聞かれる(null=False?)ので、既存のCategoryインスタンスから任意のものを選び、そのIDを入力して設定する。
  category = models.ForeignKey(Category, on_delete=models.PROTECT)
  # インスタンスを保存するフィールドを作るためにForeignKeyを使う。ForeignKeyでは、そのフィールドと紐付けるモデルを第1引数に指定する。下記では、userフィールドにUserインスタンスを保存できるようにしている。
  # on_deleteでは、紐づいたインスタンスが削除されたときの挙動を定義。CASCADEだと、Userインスタンスが削除した場合、そのユーザーと紐づいた投稿も全て削除される。
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title