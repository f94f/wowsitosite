from django.urls import path
from mountsHunt import views

urlpatterns = [
    path('', views.index, name='index'),
    path('firstLoad', views.firstLoad, name='firstLoad'),
    path('mounts', views.allMounts, name='mounts'),
    path('mount/<str:pk>', views.getMount, name='mount'),
    path('filterMounts', views.filterMounts, name='filterMounts'),
    # path('load', views.load_mounts_form_json, name='load'),
    # path('img/<int:pk>/<str:tipo>', views.img, name='img'),
]