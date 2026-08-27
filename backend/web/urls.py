from django.urls import path, re_path

from web.views.index import index

urlpatterns = [
    path('', index, name='index'),
]
