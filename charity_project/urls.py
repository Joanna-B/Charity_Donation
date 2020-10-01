"""charity_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from charity_app.views import LandingPage, AddDonation, login_view, signup_view, logout_view, UserProfile, \
                        DonationFormConfirmation, UpdateUserProfile

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', LandingPage.as_view(), name="landing-page"),
    path('add_donation/', AddDonation.as_view(), name="add-donation"),
    path('login/', login_view, name="login"),
    path('register/', signup_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('profile/', UserProfile.as_view(), name="user-profile"),
    path('update_profile/', UpdateUserProfile.as_view(), name="update-user-profile"),
    path('form_confirmation/', DonationFormConfirmation.as_view(), name="confirmation"),
]
