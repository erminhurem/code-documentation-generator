from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('generate_docs/<int:file_id>/', views.generate_docs, name='generate_docs'),
    path('files/<int:file_id>/delete/', views.delete_file, name='delete_file'),
]

