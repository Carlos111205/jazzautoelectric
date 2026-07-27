from django.db import models

class BookingRequest(models.Model):
    SERVICE_CHOICES = [
        ('diagnostics', 'Dealer-Level Diagnostic Testing'),
        ('hybrid_battery', 'Toyota Hybrid HV Battery Servicing'),
        ('dual_clutch', 'Honda GP Dual Clutch Replacement'),
        ('electrical_repairs', 'Electrical Repairs'),
        ('battery_replacement', 'Standard Battery Replacement'),
        ('alternator_starter', 'Alternator/Starter Repairs'),
        ('troubleshooting', 'General Auto-Electrical Troubleshooting'),
        ('other', 'Other Service'),
    ]

    TIME_CHOICES = [
        ('morning', 'Morning (8:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:00 PM - 5:00 PM)'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    vehicle_make = models.CharField(max_length=50, verbose_name="Vehicle Make (e.g. Toyota)")
    vehicle_model = models.CharField(max_length=50, verbose_name="Vehicle Model (e.g. Fit GP5, Prius)")
    vehicle_year = models.IntegerField(verbose_name="Vehicle Year")
    service_type = models.CharField(max_length=50, default='diagnostics')
    preferred_date = models.DateField(verbose_name="Preferred Date")
    preferred_time = models.CharField(max_length=20, choices=TIME_CHOICES, default='morning')
    message = models.TextField(blank=True, verbose_name="Additional Details or Symptoms")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.vehicle_make} {self.vehicle_model} ({self.get_service_type_display()})"

    def get_service_type_display(self):
        try:
            from .models import Service
            service = Service.objects.filter(slug=self.service_type).first()
            if service:
                return service.title
        except Exception:
            pass
        return self.service_type.replace('_', ' ').title()


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class CompanyProfile(models.Model):
    name = models.CharField(max_length=100, default='Jazz Auto Electrics')
    slogan = models.CharField(max_length=200, default='Where Precision Meets Harmony')
    phone = models.CharField(max_length=30, default='+263 71 294 8625')
    phone_raw = models.CharField(max_length=30, default='+263712948625', help_text="Digits only with country code, e.g. +263712948625")
    alt_phone = models.CharField(max_length=30, default='+263 77 425 5065')
    alt_phone_raw = models.CharField(max_length=30, default='+263774255065')
    whatsapp = models.CharField(max_length=30, default='+263 71 294 8625')
    whatsapp_url = models.TextField(default='https://wa.me/263712948625?text=Hi%20Jazz%20Auto%20Electrics,%20I%20would%20like%20to%20inquire%20about%20your%20services%20or%20motor%20spares.')
    email = models.EmailField(default='info@jazzautoelectrics.co.zw')
    address = models.TextField(default='Cold Comfort, Harare, Zimbabwe (Mobile Workshop Nationwide)')
    hours_weekdays = models.CharField(max_length=100, default='Mon - Fri: 8:00 AM - 5:00 PM')
    hours_saturday = models.CharField(max_length=100, default='Sat: 8:00 AM - 1:00 PM')
    hours_sunday = models.CharField(max_length=100, default='Sun: Closed')
    map_latitude = models.FloatField(default=-17.8228)
    map_longitude = models.FloatField(default=30.9856)

    # Social Media Links
    facebook_url = models.URLField(default='https://www.facebook.com/profile.php?id=100064758844406')
    instagram_url = models.URLField(default='https://www.instagram.com/jazz_auto_electrics/')
    tiktok_url = models.URLField(default='https://www.tiktok.com/@jazzauto_electrics')

    # Hero section content
    hero_tag = models.CharField(max_length=100, default='DEALER-LEVEL DIAGNOSTICS & HYBRID SPECIALISTS')
    hero_title = models.CharField(max_length=200, default='Dealer-Level Diagnostics & High-Precision Auto Electrics')
    hero_subtitle = models.TextField(default="Equipped with dealer-level diagnostic scanners & high-precision testing equipment. Toyota Hybrid HV battery diagnosis, balancing & cell replacement, Honda GP Dual Clutch replacement & servicing.")

    # Live Status Board content
    status_diagnostics_queue = models.CharField(max_length=100, default='Active (Cold Comfort & Mobile Workshop)')
    status_diagnostics_class = models.CharField(max_length=50, default='val-green', help_text="CSS class for styling: val-green (green), val-orange (yellow/orange), val-red (red)")
    status_location_text = models.CharField(max_length=100, default='Cold Comfort, Harare')

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profile"

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, default='fas fa-tools', help_text="FontAwesome icon class, e.g. fas fa-laptop-code")
    description = models.TextField()
    bullet_points = models.TextField(help_text="Enter bullet points, one per line")
    order = models.IntegerField(default=0, help_text="Display order sequence")

    class Meta:
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_bullet_points_list(self):
        if not self.bullet_points:
            return []
        return [p.strip() for p in self.bullet_points.split('\n') if p.strip()]

    def get_bullet_points_with_icons(self):
        points = self.get_bullet_points_list()
        result = []
        for p in points:
            if '|' in p:
                parts = p.split('|', 1)
                result.append({
                    'icon': parts[0].strip(),
                    'text': parts[1].strip()
                })
            else:
                result.append({
                    'icon': 'fas fa-check-circle',
                    'text': p
                })
        return result


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Fleet Manager, Harare Driver")
    rating = models.IntegerField(default=5, help_text="Rating out of 5 stars")
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating} stars)"

    def get_stars_range(self):
        return range(self.rating)
