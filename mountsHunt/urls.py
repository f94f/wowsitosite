from django.urls import path
from mountsHunt import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mount/<str:pk>', views.getMount, name='mount'),
    path('img/<int:pk>/<str:tipo>', views.img, name='img'),
    # path('load', views.load_mounts_form_json, name='load'),
]