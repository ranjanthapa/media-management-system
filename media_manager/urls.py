from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('delete/<int:id>/', views.delete_file, name='deleteFile'),
    path('view/<int:file_id>/', views.view_file, name='view_file'),
]