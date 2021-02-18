from django.shortcuts import render, redirect, get_object_or_404
# Userモデルはデフォルトである為、インポートすれば使える。
from django.contrib.auth.models import User
from .models import Photo, Category
# ユーザー登録用のフォーム（UserCreationForm）をインポート。
from django.contrib.auth.forms import UserCreationForm
# ユーザー登録完了と同時にログインを行うためのライブラリをインポート
from django.contrib.auth import authenticate, login
# 新規投稿機能にかかるライブラリ
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm
# メッセージを表示するライブラリ
from django.contrib import messages
# 削除にかかるライブラリ
from django.views.decorators.http import require_POST


# Create your views here.

def index(request):
    #  Photoインスタンスを全て取得する。
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'photos': photos})


def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    # Userインスタンス=>Photoインスタンスへの逆参照。特定のユーザーのphoto一覧を表示できる。シェルでクエリセットで取得できることを確認可能。
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'app/users_detail.html', {'user': user, 'photos': photos})

# ログイン機能実装では、フォームから情報を受けて自動的にログインしたが、ユーザー登録の場合は、登録処理を実装する必要がある。


def signup(request):
    if request.method == 'POST':
        # Userインスタンスを作成のみ
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # formに入力した情報でUserインスタンスを保存
            new_user = form.save()
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            # authenticate：usernameとpasswordを引数にとり、その組み合わせで認証成功すれば、Userオブジェクトを返す。できなければNone。
            new_user = authenticate(
                username=input_username, password=input_password)
            # 認証成功時のみ、Userをログインさせる。
            if new_user is not None:
                # loginメソッドは、認証できてなくてもログインさせることができてしまう。その為、authenticateで認証を行い、条件分岐した上でログインさせる為、セットで使われることが多い。 login：request情報とUserオブジェクト(new_user)を引数にとり、そのユーザーを登録と同時にログイン状態にしている。
                login(request, new_user)
                return redirect('app:users_detail', pk=new_user.pk)
    # GETの時（URLに直接pathを書いた時）
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

# @がついているのは、Pythonのデコレータという機能。@login_requiredでユーザーがログイン状態にあれば、photos_new関数を実行し、していなければ実行せず、ログイン画面（setting.pyで設定したLOGIN_URL）にリダイレクトさせる。


@login_required
def photos_new(request):
    if request.method == "POST":
        # ファイル情報(画像など)を受け取る時は、request.FILESを別記しないと正常にアップロードされない。
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # PhotoFormは、Photoモデルに紐づいたフォーム。入力された情報からPhotoインスタンスを生成。ただsaveメソッドのcommit引数をFalseにすることで、DBには保存しないようにしている。なぜなら、この段階でphotoインスタンスのuserフィールドに入れる値が決まっていないから。forms.pyで設定している[title, comment, image, category]だけ。
            photo = form.save(commit=False)
            # 一時的に生成したPhotoインスタンスのuserフィールドに、投稿者であるrequest.userを代入。フィールドへの値をTemplate上で入力しな いもの(userフィールド)については、関数内で定義してあげる必要がある。
            photo.user = request.user
            # 全てのフィールドに値が入った状態になったので、インスタンスをDBに保存。
            photo.save()
            # 成功メッセージを表示する。messageモジュールは上でインポートしてきている。
            messages.success(request, "投稿が完了しました！")
        return redirect('app:users_detail', pk=request.user.pk)
    else:
        form = PhotoForm()
    return render(request, 'app/photos_new.html', {'form': form})


def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'app/photos_detail.html', {'photo': photo})

# デコレータ(POSTリクエストのみ許可する)


@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('app:users_detail', request.user.id)

# 引き金であるcategoryを受け取る。


def photos_category(request, category):
    # title(Categoryのtitle、つまりcategory)がURLの文字列と一致するCategoryインスタンスを取得。
    category = Category.objects.get(title=category)
    # 取得したCategoryに属するPhoto一覧を取得。逆参照？
    photos = Photo.objects.filter(category=category).order_by('-created_at')
    return render(request, 'app/index.html', {'photos': photos, 'category': category})
