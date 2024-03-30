"""
URL configuration for fun_post project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from mysite import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('delpost/<int:pid>/<str:del_pass>/', views.delpost),
    path('list/', views.listing),
    path('post/', views.posting),
    path('contract/', views.contract),
    path('post2db/', views.post2db),
    path('captcha/',include('captcha.urls')),
    path('bmi/',views.bmi),
    path('delbodyinfo/<str:name>',views.delbodyinfo)
] + static(settings.MEDIA_URL ,document_root=settings.MEDIA_ROOT)

