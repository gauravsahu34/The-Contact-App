from django.urls import path
from . import views


app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('about/',views.about, name='about'),
    path('contact/<int:id>/', views.contact_detail, name='contact_detail'),
    path('contact/send/<int:id>/', views.send_message, name='send_message'),
    path('contact/sendotp/<int:id>/', views.send_otp,name='send_otp'),
    path('contact/messages/',views.messages_list,name='messages_list')
]
