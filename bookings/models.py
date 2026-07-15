from django.db import models

class BookingRequest(models.Model):
    SERVICE_CHOICES = [
        ('diagnostics', 'Diagnostic Testing'),
        ('electrical_repairs', 'Electrical Repairs'),
        ('battery_replacement', 'Battery Replacement'),
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
    vehicle_model = models.CharField(max_length=50, verbose_name="Vehicle Model (e.g. Hilux)")
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
    name = models.CharField(max_length=100, default='Jazz Auto Electric')
    phone = models.CharField(max_length=30, default='+263 77 245 6789')
    phone_raw = models.CharField(max_length=30, default='+263772456789', help_text="Digits only with country code, e.g. +263772456789")
    whatsapp = models.CharField(max_length=30, default='+263 77 245 6789')
    whatsapp_url = models.TextField(default='https://wa.me/263772456789?text=Hi%20Jazz%20Auto%20Electric,%20I%20would%20like%20to%20inquire%20about%20your%20services%20or%20motor%20spares.')
    email = models.EmailField(default='info@jazzautoelectric.co.zw')
    address = models.TextField(default='Plot 104, Cripps Road, Graniteside, Harare, Zimbabwe')
    hours_weekdays = models.CharField(max_length=100, default='Mon - Fri: 8:00 AM - 5:00 PM')
    hours_saturday = models.CharField(max_length=100, default='Sat: 8:00 AM - 1:00 PM')
    hours_sunday = models.CharField(max_length=100, default='Sun: Closed')
    map_latitude = models.FloatField(default=-17.8485)
    map_longitude = models.FloatField(default=31.0605)

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
