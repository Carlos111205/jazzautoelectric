from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookingForm, ContactForm, OwnerRegisterForm, OwnerLoginForm
from .models import Service, Testimonial
from inventory.models import Category, Part

def home(request):
    # Fetch 4 items in stock for the spares preview section
    featured_parts = Part.objects.filter(is_available=True)[:4]
    services_list = Service.objects.all()[:3]
    testimonials_list = Testimonial.objects.filter(is_active=True)[:3]
    categories_list = Category.objects.all()[:4]
    
    context = {
        'featured_parts': featured_parts,
        'services': services_list,
        'testimonials': testimonials_list,
        'categories': categories_list
    }
    return render(request, 'home.html', context)

def services(request):
    services_list = Service.objects.all()
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return render(request, 'booking_success.html', {
                'type': 'booking',
                'booking': booking
            })
    else:
        # Allow pre-selecting a service type via query parameters (e.g. from service cards)
        initial_service = request.GET.get('service', 'diagnostics')
        form = BookingForm(initial={'service_type': initial_service})
        
    return render(request, 'services.html', {
        'form': form,
        'services': services_list
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            return render(request, 'booking_success.html', {
                'type': 'contact',
                'inquiry': inquiry
            })
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'form': form})

def owner_register(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin/')

    error_msg = None
    if request.method == 'POST':
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            if User.objects.filter(username=username).exists():
                error_msg = f"Username '{username}' is already taken. Please choose another."
            elif User.objects.filter(email=email).exists():
                error_msg = f"Email '{email}' is already registered. Please log in or use a different email."
            else:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                login(request, user)
                messages.success(request, f"Welcome {first_name}! Owner account created successfully.")
                return redirect('/admin/')
    else:
        form = OwnerRegisterForm()

    return render(request, 'owner_register.html', {
        'form': form,
        'error_msg': error_msg
    })

def owner_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/admin/')

    error_msg = None
    if request.method == 'POST':
        form = OwnerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Allow logging in with either username or email
            if '@' in username:
                user_obj = User.objects.filter(email__iexact=username).first()
                if user_obj:
                    username = user_obj.username

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/admin/')
            else:
                error_msg = "Invalid username/email or password. Please try again."
    else:
        form = OwnerLoginForm()

    return render(request, 'owner_login.html', {
        'form': form,
        'error_msg': error_msg
    })

def owner_logout(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('bookings:home')

