from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('ingenieria-sistemas/entries/', views.entry_list, name='ingenieria_sistemas_entries'),
    path('ingenieria-sistemas/entry/<int:pk>/', views.entry_detail, name='ingenieria_sistemas_entry_detail'),
    path('entry/new/', views.entry_new, name='entry_new'),
    path('entry/<int:pk>/edit/', views.edit_entry, name='entry_edit'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('extracted-data/', views.extracted_data_list, name='extracted_data_list'),
]
