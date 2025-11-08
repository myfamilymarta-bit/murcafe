from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/', views.cats_list, name='cats'),
    path('cats/<int:cat_id>/', views.cat_detail, name='cats_detail'),
    path('staff/', views.staff_page, name='staff'),
    path('reviews/', views.submit_review, name='submit_review'),
    path('menu/', views.menu_page, name='menu'),
    path('help/', views.help_page, name='help'),
    path('contact/', views.contact_form, name='contact'),
    path('api/cats/', api.CatListApiView.as_view(), name='api_cats'),
    path('api/menu/', api.MenuItemListApiView.as_view(), name='api_menu'),
    path('api/reviews/', api.StaffReviewListApiView.as_view(), name='api_review'),
    path('api/staff/', api.StaffListApiView.as_view(), name='api_staff'),
    path('api/messages', api.ContactMessageListApiView.as_view(), name='api_message'),
]
from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/', views.cats_list, name='cats'),
    path('cats/<int:cat_id>/', views.cat_detail, name='cats_detail'),
    path('staff/', views.staff_page, name='staff'),
    path('reviews/', views.submit_review, name='submit_review'),
    path('menu/', views.menu_page, name='menu'),
    path('help/', views.help_page, name='help'),
    path('contact/', views.contact_form, name='contact'),
    path('api/cats/', api.CatListApiView.as_view(), name='api_cats'),
    path('api/menu/', api.MenuItemListApiView.as_view(), name='api_menu'),
    path('api/reviews/', api.StaffReviewListApiView.as_view(), name='api_review'),
    path('api/staff/', api.StaffListApiView.as_view(), name='api_staff'),
    path('api/messages', api.ContactMessageListApiView.as_view(), name='api_message'),
]
