from django import forms
from .models import BookingRequest, ContactInquiry

class BookingForm(forms.ModelForm):
    service_type = forms.ChoiceField(
        choices=[
            ('diagnostics', 'Diagnostic Testing'),
            ('electrical_repairs', 'Electrical Repairs'),
            ('battery_replacement', 'Battery Replacement'),
            ('alternator_starter', 'Alternator/Starter Repairs'),
            ('troubleshooting', 'General Auto-Electrical Troubleshooting'),
        ],
        label="Service Needed"
    )

    class Meta:
        model = BookingRequest
        fields = [
            'name', 'email', 'phone', 
            'vehicle_make', 'vehicle_model', 'vehicle_year', 
            'service_type', 'preferred_date', 'preferred_time', 
            'message'
        ]
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically load choices from Service model in database
        try:
            from .models import Service
            services = Service.objects.all()
            if services.exists():
                self.fields['service_type'].choices = [(s.slug, s.title) for s in services]
        except Exception:
            # Fallback if table doesn't exist yet during initial setup
            pass

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['placeholder'] = f"Enter {field.label}"
            # Custom placeholders where helpful
            if field_name == 'vehicle_make':
                field.widget.attrs['placeholder'] = "e.g., Toyota"
            elif field_name == 'vehicle_model':
                field.widget.attrs['placeholder'] = "e.g., Hilux"
            elif field_name == 'vehicle_year':
                field.widget.attrs['placeholder'] = "e.g., 2018"
            elif field_name == 'message':
                field.widget.attrs['placeholder'] = "Describe the symptoms (e.g. battery draining, engine misfire)..."


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['placeholder'] = f"Enter your {field_name.replace('_', ' ')}"
            if field_name == 'message':
                field.widget.attrs['placeholder'] = "Write your message here..."
