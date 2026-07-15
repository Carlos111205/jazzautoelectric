from django.contrib import admin
from .models import BookingRequest, ContactInquiry, CompanyProfile, Service, Testimonial

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'vehicle_make', 'vehicle_model', 'service_type', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'service_type', 'preferred_date', 'created_at')
    search_fields = ('name', 'email', 'phone', 'vehicle_make', 'vehicle_model', 'message')
    list_editable = ('status',)
    date_hierarchy = 'preferred_date'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'service_type':
            from django import forms
            from .models import Service
            try:
                services = Service.objects.all()
                choices = [(s.slug, s.title) for s in services]
                if not choices:
                    choices = [('diagnostics', 'Diagnostic Testing')]
            except Exception:
                choices = [('diagnostics', 'Diagnostic Testing')]
            return forms.ChoiceField(choices=choices, label=db_field.verbose_name)
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'hours_weekdays')
    # Limit creation of company profiles so the owner doesn't create multiple config profiles
    def has_add_permission(self, request):
        return not CompanyProfile.objects.exists()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'icon_class', 'order')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    search_fields = ('title', 'description', 'bullet_points')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'role', 'text')
    list_editable = ('is_active', 'rating')
