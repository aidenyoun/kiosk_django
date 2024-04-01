from django.urls import path
from . import views
from .views import save_profile_data

urlpatterns = [
    path("", views.upload_video, name='index'),
    path('save_profile_data/', save_profile_data, name='save_profile_data'),
]
