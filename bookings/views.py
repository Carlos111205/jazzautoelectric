import urllib.parse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import BookingForm, ContactForm, OwnerLoginForm
from .models import Service, Testimonial, CompanyProfile
from inventory.models import Category, Part

def get_whatsapp_phone():
    profile = CompanyProfile.objects.first()
    if profile and profile.whatsapp:
        # Extract digits only
        phone_digits = ''.join(c for c in profile.whatsapp if c.isdigit())
        if phone_digits:
            return phone_digits
    return "263712948625"

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
            
            # Direct WhatsApp message formatting for instant communication
            msg = (
                f"Hi Jazz Auto Electrics, I would like to book a repair service:\n\n"
                f"👤 *Name:* {booking.name}\n"
                f"📞 *Phone:* {booking.phone}\n"
                f"✉️ *Email:* {booking.email}\n"
                f"🚗 *Vehicle:* {booking.vehicle_make} {booking.vehicle_model} ({booking.vehicle_year})\n"
                f"🔧 *Service Requested:* {booking.get_service_type_display()}\n"
                f"📅 *Preferred Date:* {booking.preferred_date} ({booking.get_preferred_time_display()})\n"
            )
            if booking.message:
                msg += f"📝 *Symptoms/Details:*\n{booking.message}\n"

            phone = get_whatsapp_phone()
            encoded_msg = urllib.parse.quote(msg)
            whatsapp_url = f"https://wa.me/{phone}?text={encoded_msg}"

            return redirect(whatsapp_url)
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
            
            # Direct WhatsApp message formatting for contact inquiries
            msg = (
                f"Hi Jazz Auto Electrics, I have an inquiry:\n\n"
                f"👤 *Name:* {inquiry.name}\n"
                f"✉️ *Email:* {inquiry.email}\n"
            )
            if inquiry.phone:
                msg += f"📞 *Phone:* {inquiry.phone}\n"
            msg += f"📌 *Subject:* {inquiry.subject}\n"
            msg += f"💬 *Message:*\n{inquiry.message}\n"

            phone = get_whatsapp_phone()
            encoded_msg = urllib.parse.quote(msg)
            whatsapp_url = f"https://wa.me/{phone}?text={encoded_msg}"

            return redirect(whatsapp_url)
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'form': form})

def owner_register(request):
    # Registration is strictly restricted to authenticated superusers/admins only
    if not (request.user.is_authenticated and request.user.is_superuser):
        messages.error(request, "Access Denied: Only the main Admin can add or grant permissions to new users.")
        return redirect('/admin/auth/user/add/' if request.user.is_authenticated else 'bookings:owner_login')

    return redirect('/admin/auth/user/add/')

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
                if user.is_staff or user.is_superuser:
                    login(request, user)
                    return redirect('/admin/')
                else:
                    error_msg = "Access Restricted: Only authorized admin accounts can enter the Jazz Control Panel."
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


