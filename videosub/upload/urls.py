from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_display_video, name='upload_display_video'),
    path('<str:id>', views.search_subs, name='search_subs'),
]