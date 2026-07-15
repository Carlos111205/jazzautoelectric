from django.shortcuts import render, redirect
from .forms import BookingForm, ContactForm
from .models import Service, Testimonial
from inventory.models import Part

def home(request):
    # Fetch 4 items in stock for the spares preview section
    featured_parts = Part.objects.filter(is_available=True)[:4]
    services_list = Service.objects.all()[:3]
    testimonials_list = Testimonial.objects.filter(is_active=True)[:3]
    
    context = {
        'featured_parts': featured_parts,
        'services': services_list,
        'testimonials': testimonials_list
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
