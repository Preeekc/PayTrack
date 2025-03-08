from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main pages
    path('', views.landing_page, name='landing_page'),
    path('service/', views.service_page, name='service_page'),
    path('about/', views.about_page, name='about_page'),
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('login/verify-otp/', views.login_verify_otp_view, name='login_verify_otp'),
    path('password-reset/', views.password_reset_request_view, name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_view, name='password_reset'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('home/', views.home_view, name='home'),
    
    # Property general browsing
    path('properties/', views.properties_list, name='properties_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
     path('view_properties/<int:pk>/', views.view_property_detail, name='view_property_detail'),

    
    # Homeowner property management
    path('my-properties/', views.property_list, name='property_list'),
    path('my-properties/add/', views.add_property, name='add_property'),
    path('my-properties/edit/<int:property_id>/', views.edit_property, name='edit_property'),
    path('my-properties/delete/<int:property_id>/', views.delete_property, name='delete_property'),
 
    # Other Dashboard Features
    path('bookings/', views.booking_list, name='booking_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings_view, name='settings'),
    path('payments/', views.payment_details, name='payment_details'),
    path('transactions/', views.transactions, name='transactions'),
    path('reports/', views.report, name='report'),
]

# Serve media files in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)