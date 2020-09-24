from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from .models import Donation, Institution
from .forms import RegistrationForm, CustomUserAuthenticationForm


class LandingPage(View):
    def get(self, request):
        donations = Donation.objects.all()
        donation_number = sum(d.quantity for d in donations)
        institution_list = []
        for d in donations:
            institution_list.append(d.institution)
        institution_qty = len(set(institution_list))
        institution_foundation = Institution.objects.filter(type=1)
        institution_ngo = Institution.objects.filter(type=2)
        institution_local = Institution.objects.filter(type=3)
        ctx = {
            'donation_number': donation_number,
            'institution_qty': institution_qty,
            'institution_foundation': institution_foundation,
            'institution_ngo': institution_ngo,
            'institution_local': institution_local,
            }
        return render(request, 'index.html', ctx)


class AddDonation(View):
    def get(self, request):
        return render(request, "form.html")


def signup_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            customuser = authenticate(email=email, password=raw_password)
            login(request, customuser)
            return redirect('login')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'register.html', context)


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("landing-page")

    if request.POST:
        form = CustomUserAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("landing-page")

            if user is None:
                return redirect("register")
    else:
        form = CustomUserAuthenticationForm()

    context['login_form'] = form
    return render(request, "login.html", context)