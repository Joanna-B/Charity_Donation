from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from .models import Donation, Institution, Category, CustomUser
from .forms import RegistrationForm, CustomUserAuthenticationForm, AddDonationForm, UserProfileForm
from django.views.generic import TemplateView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy



class LandingPage(View):
    def get(self, request):
        donations = Donation.objects.all()
        donation_number = sum(d.quantity for d in donations)
        institution_list = []
        for d in donations:
            institution_list.append(d.institution)
        institution_qty = len(set(institution_list))
        foundation_list = Institution.objects.filter(type=1)
        ngo_list = Institution.objects.filter(type=2)
        local_list = Institution.objects.filter(type=3)
        page = request.GET.get('page', 1)

        paginator = Paginator(foundation_list, 5)
        try:
            foundations = paginator.page(page)
        except PageNotAnInteger:
            foundations = paginator.page(1)
        except EmptyPage:
            foundations = paginator.page(paginator.num_pages)

        paginator = Paginator(ngo_list, 5)
        try:
            ngos = paginator.page(page)
        except PageNotAnInteger:
            ngos = paginator.page(1)
        except EmptyPage:
            ngos = paginator.page(paginator.num_pages)

        paginator = Paginator(local_list, 5)
        try:
            locals = paginator.page(page)
        except PageNotAnInteger:
            locals = paginator.page(1)
        except EmptyPage:
            locals = paginator.page(paginator.num_pages)

        ctx = {
            'donation_number': donation_number,
            'institution_qty': institution_qty,
            'foundation_list': foundation_list,
            'ngo_list': ngo_list,
            'institution_local': local_list,
            'foundations': foundations,
            'ngos': ngos,
            'locals': locals,
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

    def post(self, request):
        form = AddDonationForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('bags')
            address = form.cleaned_data.get('address')
            phone_number = form.cleaned_data.get('phone')
            city = form.cleaned_data.get('city')
            zip_code = form.cleaned_data.get('postcode')
            pick_up_date = form.cleaned_data.get('date')
            pick_up_time = form.cleaned_data.get('time')
            pick_up_comment = form.cleaned_data.get('more_info')
            categories = form.cleaned_data.get('categories')
            institution = form.cleaned_data.get('organization')
            # organization = form.cleaned_data.get('organization')
            # institution = Institution.objects.get(id=organization)
            user = request.user

            new_donation = Donation.objects.create(quantity=quantity, address=address, phone_number=phone_number,
                                                   city=city, zip_code=zip_code, pick_up_date=pick_up_date,
                                                   pick_up_time=pick_up_time, pick_up_comment=pick_up_comment,
                                                   institution=institution, user=user)
            new_donation.save()
            new_donation.categories.add(categories)

            return render(request, "form-confirmation.html")


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


class DonationFormConfirmation(TemplateView):
    template_name = 'form-confirmation.html'

class UpdateUserProfile(UpdateView):
    model = CustomUser
    form = UserProfileForm
    fields = '__all__'
    success_url = reverse_lazy('userprofile.html')







