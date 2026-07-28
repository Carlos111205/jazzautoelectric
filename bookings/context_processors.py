from .models import CompanyProfile

def business_info(request):
    profile = CompanyProfile.objects.first()
    if profile:
        return {
            'BUSINESS_NAME': profile.name,
            'BUSINESS_SLOGAN': profile.slogan,
            'BUSINESS_PHONE': profile.phone,
            'BUSINESS_PHONE_RAW': profile.phone_raw,
            'BUSINESS_ALT_PHONE': profile.alt_phone,
            'BUSINESS_ALT_PHONE_RAW': profile.alt_phone_raw,
            'BUSINESS_WHATSAPP': profile.whatsapp,
            'BUSINESS_WHATSAPP_URL': profile.whatsapp_url,
            'BUSINESS_FACEBOOK_URL': profile.facebook_url,
            'BUSINESS_INSTAGRAM_URL': profile.instagram_url,
            'BUSINESS_TIKTOK_URL': profile.tiktok_url,
            'BUSINESS_EMAIL': profile.email,
            'BUSINESS_ADDRESS': profile.address,
            'BUSINESS_HOURS_WEEKDAYS': profile.hours_weekdays,
            'BUSINESS_HOURS_SATURDAY': profile.hours_saturday,
            'BUSINESS_HOURS_SUNDAY': profile.hours_sunday,
            'MAP_LATITUDE': profile.map_latitude,
            'MAP_LONGITUDE': profile.map_longitude,
            'HERO_TAG': profile.hero_tag,
            'HERO_TITLE': profile.hero_title,
            'HERO_SUBTITLE': profile.hero_subtitle,
            'STATUS_DIAGNOSTICS_QUEUE': profile.status_diagnostics_queue,
            'STATUS_DIAGNOSTICS_CLASS': profile.status_diagnostics_class,
            'STATUS_LOCATION_TEXT': profile.status_location_text,
        }
    
    # Fallback default values
    return {
        'BUSINESS_NAME': 'Jazz Auto Electrics',
        'BUSINESS_SLOGAN': 'Where Precision Meets Harmony',
        'BUSINESS_PHONE': '+263 71 294 8625',
        'BUSINESS_PHONE_RAW': '+263712948625',
        'BUSINESS_ALT_PHONE': '+263 77 425 5065',
        'BUSINESS_ALT_PHONE_RAW': '+263774255065',
        'BUSINESS_WHATSAPP': '+263 71 294 8625',
        'BUSINESS_WHATSAPP_URL': 'https://wa.me/263712948625?text=Hi%20Jazz%20Auto%20Electrics,%20I%20would%20like%20to%20inquire%20about%20your%20services%20or%20motor%20spares.',
        'BUSINESS_FACEBOOK_URL': 'https://www.facebook.com/profile.php?id=100064758844406',
        'BUSINESS_INSTAGRAM_URL': 'https://www.instagram.com/jazz_auto_electrics/',
        'BUSINESS_TIKTOK_URL': 'https://www.tiktok.com/@jazzauto_electrics',
        'BUSINESS_EMAIL': 'imionjali5@gmail.com',
        'BUSINESS_ADDRESS': 'Cold Comfort, Harare, Zimbabwe (Mobile Workshop Nationwide)',
        'BUSINESS_HOURS_WEEKDAYS': 'Mon - Fri: 8:00 AM - 5:00 PM',
        'BUSINESS_HOURS_SATURDAY': 'Sat: 8:00 AM - 1:00 PM',
        'BUSINESS_HOURS_SUNDAY': 'Sun: Closed',
        'MAP_LATITUDE': -17.8228,
        'MAP_LONGITUDE': 30.9856,
        'HERO_TAG': 'DEALER-LEVEL DIAGNOSTICS & HYBRID SPECIALISTS',
        'HERO_TITLE': 'Dealer-Level Diagnostics & High-Precision Auto Electrics',
        'HERO_SUBTITLE': "Equipped with dealer-level diagnostic scanners and high-precision testing equipment. We specialize in Toyota Hybrid HV battery diagnosis, voltage balancing & cell replacement, Honda GP dual clutch replacements & servicing.",
        'STATUS_DIAGNOSTICS_QUEUE': 'Active (Cold Comfort & Mobile Workshop)',
        'STATUS_DIAGNOSTICS_CLASS': 'val-green',
        'STATUS_LOCATION_TEXT': 'Cold Comfort, Harare',
    }
