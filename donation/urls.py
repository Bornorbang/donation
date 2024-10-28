"""
URL configuration for donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('projects/', views.project, name="projects"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('donate-for-wealthy/', views.donatewealthy, name='donatewealthy'),
    path('raise-to-raise/', views.raisetoraise, name='raisetoraise'),
    path('zakat/', views.zakat, name="zakat"),
    path('donation-history/', views.donation_history, name="donation_history"),
    path('project/<int:project_id>/', views.project_detail, name="project_detail"),
    path('donate/<int:project_id>/', views.donate, name="donate"),
    path('checkout/<int:project_id>/<int:donate_id>/', views.checkout, name='checkout'),
    path('payment-success/<int:project_id>/<int:donate_id>/', views.PaymentSuccess, name='payment_success'),
    path('payment-failure/<int:project_id>/<int:donate_id>/', views.PaymentFailure, name='payment_failure'),
    path('aboutus/', views.aboutus, name="aboutus"),
    path('bankaccounts/', views.bankaccounts, name="bankaccounts"),
    path('', include('paypal.standard.ipn.urls')),
    path('stripe-checkout/<int:project_id>/<int:donate_id>/', views.stripe_checkout, name='stripe_checkout'),
]
