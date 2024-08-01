from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    #path('ingenieria_sistemas/', views.ingenieria_sistemas_view, name='ingenieria_sistemas'),
    path('detail/<int:pk>/', detail_page, name='detail_page'),
    path('entries/', views.entry_list, name='entry_list'),
    #path('entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entry/new/', views.entry_new, name='entry_new'),
    #_________path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('extracted-data/', views.extracted_data_list, name='extracted_data_list'),
    #path('', base, name='base'),

    ##para la sección de ingenieria de sistemas
    path('ingenieria-sistemas/entries/', views.entry_list, name='ingenieria_sistemas_entries'),
    path('ingenieria-sistemas/entry/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entry/<int:pk>/edit/', views.edit_entry, name='entry_edit'),

]
