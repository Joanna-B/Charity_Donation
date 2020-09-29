from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import Donation, Institution, Category, CustomUser
from .forms import RegistrationForm, CustomUserAuthenticationForm, AddDonationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required


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
    form = AddDonationForm()
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        if request.user.is_authenticated:
            return render(request, "form.html", ctx)
        else:
            return render(request, "login.html")

    # def post(self, request):
    #     form = AddDonationForm(request.POST)
    #     ctx = {"form": form}
    #     if form.is_valid():
    #         quantity = request.POST.get('bags')
    #         address = request.POST.get('address')
    #         phone_number = request.POST.get('phone')
    #         city = request.POST.get('city')
    #         zip_code = request.POST.get('postcode')
    #         pick_up_date = request.POST.get('date')
    #         pick_up_time = request.POST.get('time')
    #         pick_up_comment = request.POST.get('more_info')
    #         categories = request.POST.getlist('categories')
    #         institution = request.POST.get('organization')
    #         user = get_object_or_404(CustomUser, id=request.user.id)
    #
    #         new_donation = Donation.objects.create(quantity=quantity, address=address, phone_number=phone_number,
    #                                                city=city, zip_code=zip_code, pick_up_date=pick_up_date,
    #                                                pick_up_time=pick_up_time, pick_up_comment=pick_up_comment,
    #                                                categories=categories, institution=institution, user=user)
    #         new_donation.save()
    #
    #     return render(request, "form-confirmation.html", ctx)


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
            return render(request, 'register.html', context)
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
        email = request.POST['email']

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("landing-page")
        else:
            if CustomUser.objects.filter(email=email).exists() is False:
                return redirect("register")

    else:
        form = CustomUserAuthenticationForm()

    context['login_form'] = form
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect('landing-page')


class UserProfile(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            donations = Donation.objects.filter(user=user)
            ctx = {
                'donations': donations,
            }
            return render(request, "userprofile.html", ctx)
        else:
            return redirect('login')


class DonationFormConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')