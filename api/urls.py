from django.urls import path
from . import views

urlpatterns = [    path('suvlar/', views.SuvListCreateView.as_view(), name='suv-list'),
    path('suvlar/<int:pk>/', views.SuvDetailView.as_view(), name='suv-detail'),


    path('mijozlar/', views.MijozListCreateView.as_view(), name='mijoz-list'),
    path('mijozlar/<int:pk>/', views.MijozDetailView.as_view(), name='mijoz-detail'),


    path('buyurtmalar/', views.BuyurtmaListCreateView.as_view(), name='buyurtma-list'),


    path('adminlar/', views.AdminListView.as_view(), name='admin-list'),
    path('adminlar/<int:pk>/', views.AdminDetailView.as_view(), name='admin-detail'),


    path('haydovchilar/', views.HaydovchiListView.as_view(), name='haydovchi-list'),
    path('haydovchilar/<int:pk>/', views.HaydovchiDetailView.as_view(), name='haydovchi-detail'),
]
