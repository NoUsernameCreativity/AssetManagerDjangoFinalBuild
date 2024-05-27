"""
Asset_Manager_v0.1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
import DjangoApp1.views # import views
from django.urls import include, re_path, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # r stands for raw, and that part at the start determines site-relative urls
    re_path(r'^$', DjangoApp1.views.index, name='index'),
    re_path(r'^home$', DjangoApp1.views.index, name='home'),
    # account authentification URLS
    path("accounts/", include("django.contrib.auth.urls")),
    # other stuff
    re_path(r'^users$', DjangoApp1.views.UsersPage, name='users'),
    re_path(r'^assets$', DjangoApp1.views.AssetsPage, name='assets'),
    re_path(r'^asset_events$', DjangoApp1.views.AssetEventsPage, name='events'),
    re_path(r'^selected_assets$', DjangoApp1.views.SelectedAssetsPage, name='selected_assets'),
    re_path(r'^accounts/sign_up$', DjangoApp1.views.SignUpPage, name='sign_up')
]

# For images.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
