from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('load', views.load_mounts_form_json, name='load'),
]