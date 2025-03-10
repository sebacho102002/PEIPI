from django.urls import path
from . import views  # Importamos solo views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('detail/<int:pk>/', views.detail_page, name='detail_page'),
    path('entries/', views.entry_list, name='entry_list'),
    path('entry/new/', views.entry_new, name='entry_new'),
    path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),  # Corrección aquí
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('extracted-data/', views.extracted_data_list, name='extracted_data_list'),

    # Sección de ingeniería de sistemas
    path('ingenieria-sistemas/entries/', views.entry_list, name='ingenieria_sistemas_entries'),
    path('ingenieria-sistemas/entry/<int:pk>/', views.entry_detail, name='entry_detail'),
]
