"""
Django settings for django_photoservice project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3^hj)$#24@c@y_i3%s=dv@9)lbs@l1&axu7$$!8no9-jy2!z^f'

# SECURITY WARNING: don't run with debug turned on in production!
# osを使って、DEBUGという環境変数(Heroku側でDEBUG="False"と指定)の値をos.environ.get("環境変数名")で取得。=> "False"=="True"となり、DEBUG="False"が返ってくることになる。
DEBUG = os.environ.get("DEBUG") == "True"

# Herokuで作製されたURLをここに格納する。ここに入れないまま検索しても、エラーメッセージが出てくる。
ALLOWED_HOSTS = ["djangophotoservice.herokuapp.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    # django_cleanupをインストールする事でPhotoインスタンスの削除と同時に画像ファイルもディレクトリから削除される。
    'django_cleanup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_photoservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_photoservice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# 開発環境で使うDBを定義している。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# デフォルトであるSTARTIC_URLでは、アプリ内にあるstaticディレクトリしか読み込まれない。※Memoアプリではアプリ内に作成した。
STATIC_URL = '/static/'
# プロジェクトディレクトリ直下のstaticディレクトリも読み込みたい場合は、以下のようにSTATICFILES_DIRSを設定。osモジュールはインポートが必要。
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = 'staticfiles'

# 画像の保存先を表すものでBASE_DIR（ルートディレクトリ）直下のmediaというディレクトリに保存される事になる。※ディレクトリは、1つ目の画像がアップロードされたタイミングで自動生成される。
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDEA_URLは、ユーザーが生成したコンテンツのURLを表すのに使われる。photo.image.urlで画像のアドレスを取得できるのだが、その際、MEDIA＿URL／photos／IMG_01.JPGのように、頭にはMEDIA＿URLに指定した文字列が入る。今回は、mediaと設定しているので、頭がmediaに置き換わってURLに表示される。
# MEDIA＿URLは、ユーザーが生成したコンテンツのURLを表す。
MEDIA_URL = '/media/'

# ログインする時に使うページを設定（login.htmlのこと）。
LOGIN_URL = 'app:login' 
# ユーザーがログインした時に最初にリダイレクトされるURLを指定（index.html）。
LOGIN_REDIRECT_URL = 'app:index' 
# ログアウトしたユーザーをリダイレクトさせるURLを指定。
LOGOUT_REDIRECT_URL = 'app:index'

# DEBUG=="False"の時、要はHeroku(本番)環境の時。
if not DEBUG:
    import django_heroku
    import dj_database_url
    # 上の方で定義しているdefaultのDBはWeb上では使えない為、ここで上書きしている。Herokuには、postgresqlというdefaultのDBがあるのでそれを使うようにする。
    # dj_database_url(パッケージ)を使えば、環境変数(DATABASE_URL)を拾ってこれる。※今回の場合は、Herokuのダッシュボードから確認可能。
    DATABASES["default"].update(dj_database_url.config(conn_max_age=600,ssl_require=True))
    # .settings = 本番環境用の設定をしてくれる。
    # https://github.com/heroku/django-heroku/blob/master/django_heroku/core.py#L49
    django_heroku.settings(locals())
