from .models import CompanyProfile

def business_info(request):
    profile = CompanyProfile.objects.first()
    if profile:
        return {
            'BUSINESS_NAME': profile.name,
            'BUSINESS_PHONE': profile.phone,
            'BUSINESS_PHONE_RAW': profile.phone_raw,
            'BUSINESS_WHATSAPP': profile.whatsapp,
            'BUSINESS_WHATSAPP_URL': profile.whatsapp_url,
            'BUSINESS_EMAIL': profile.email,
            'BUSINESS_ADDRESS': profile.address,
            'BUSINESS_HOURS_WEEKDAYS': profile.hours_weekdays,
            'BUSINESS_HOURS_SATURDAY': profile.hours_saturday,
            'BUSINESS_HOURS_SUNDAY': profile.hours_sunday,
            'MAP_LATITUDE': profile.map_latitude,
            'MAP_LONGITUDE': profile.map_longitude,
        }
    
    # Fallback default values
    return {
        'BUSINESS_NAME': 'Jazz Auto Electric',
        'BUSINESS_PHONE': '+263 77 245 6789',
        'BUSINESS_PHONE_RAW': '+263772456789',
        'BUSINESS_WHATSAPP': '+263 77 245 6789',
        'BUSINESS_WHATSAPP_URL': 'https://wa.me/263772456789?text=Hi%20Jazz%20Auto%20Electric,%20I%20would%20like%20to%20inquire%20about%20your%20services%20or%20motor%20spares.',
        'BUSINESS_EMAIL': 'info@jazzautoelectric.co.zw',
        'BUSINESS_ADDRESS': 'Plot 104, Cripps Road, Graniteside, Harare, Zimbabwe',
        'BUSINESS_HOURS_WEEKDAYS': 'Mon - Fri: 8:00 AM - 5:00 PM',
        'BUSINESS_HOURS_SATURDAY': 'Sat: 8:00 AM - 1:00 PM',
        'BUSINESS_HOURS_SUNDAY': 'Sun: Closed',
        'MAP_LATITUDE': -17.8485,
        'MAP_LONGITUDE': 31.0605,
    }
