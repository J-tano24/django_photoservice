from django.urls import path
from . import views
# auth_viewsライブラリでは、自動的にログイン／ログアウトしてくれるLoginViewとLogoutViewという関数が使える。viewsでの関数作成は不要。
from django.contrib.auth import views as auth_views

app_name = 'app'
urlpatterns = [
  path('', views.index, name='index'),
  path('users/<int:pk>/', views.users_detail, name='users_detail'),
  path('photos/new/', views.photos_new, name='photos_new'),
  path('photos/<int:pk>/', views.photos_detail, name='photos_detail'),
  path('photos/<int:pk>/delete/', views.photos_delete, name='photos_delete'),
  # 引き金となる文字列categoryをviewsの関数に渡す。
  path('photos/<str:category>/', views.photos_category, name='photos_category'),
  path('signup/', views.signup, name='signup'),
  # ログイン画面のURL、ユーザーがログインした後にリダイレクトされるURL、ログアウトした後にリダイレクトされるURLの設定が必要。
  # LoginViewsでは、引数template_nameにログイン画面となるHTMLファイルのパスを指定する。
  path('login/', auth_views.LoginView.as_view(template_name='app/login.html'),name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]