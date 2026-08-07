from django.urls import path
from . import views

urlpatterns = [
    path('', views.enquiry, name='enquiry'),
    path('create/', views.create_enquiry, name='create_enquiry'),
    path('reply/<int:id>/', views.reply_enquiry, name='reply_enquiry'),
    path('enquiry-list/', views.enquiry_list, name='enquiry_list'),
]