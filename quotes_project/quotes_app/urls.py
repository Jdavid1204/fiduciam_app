"""quotes_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.urls import include
from quotes_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scrape/', views.scrape, name='scrape'),
    path('author/<int:author_id>/', views.quotes_by_author, name='quotes_by_author'),
    path('tag/<int:tag_id>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('download/', views.download, name='download'),
    path('delete/', views.delete_quotes, name='delete_quotes'),
]
