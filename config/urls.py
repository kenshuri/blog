"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

import core.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core.views.index, name='index'),
    path('posts/', core.views.posts, name='posts'),
    path('posts/<str:postname>', core.views.view_post, name='view_post'),
    path('books/', core.views.books, name='books'),
    path('about/', core.views.about, name='about'),
    path("__reload__/", include("django_browser_reload.urls")),
]

htmx_urlpatterns = [
    path('post_search/', core.views.post_search, name='post_search'),
    path('book_search/', core.views.book_search, name='book_search'),
    path('books/<int:stars>', core.views.book_filter, name='book_filter'),
]

urlpatterns += htmx_urlpatterns