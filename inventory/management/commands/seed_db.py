from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Category, Part
from bookings.models import CompanyProfile, Service, Testimonial

class Command(BaseCommand):
    help = 'Seeds the database with realistic auto-electrical parts, categories, services, and profile'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # 1. Clear existing data
        Part.objects.all().delete()
        Category.objects.all().delete()
        CompanyProfile.objects.all().delete()
        Service.objects.all().delete()
        Testimonial.objects.all().delete()
        
        # 2. Create Categories
        # 2. Create Categories
        categories_data = [
            {
                'name': 'Toyota Hybrid Components',
                'description': 'High-voltage hybrid battery cells, modules, balancing harnesses, and cooling blowers.',
                'icon_class': 'fas fa-car-battery'
            },
            {
                'name': 'Honda Dual Clutch Parts',
                'description': 'Honda GP series dual clutch sets, release bearings, actuator fluids, and sensor modules.',
                'icon_class': 'fas fa-cogs'
            },
            {
                'name': 'Batteries & Charging',
                'description': 'Premium automotive AGM batteries, heavy-duty terminals, testers, and power management.',
                'icon_class': 'fas fa-bolt'
            },
            {
                'name': 'Starters & Alternators',
                'description': 'Heavy-duty starter motors, high-output alternators, regulators, solenoids, and diode plates.',
                'icon_class': 'fas fa-sync-alt'
            },
            {
                'name': 'Sensors & Engine Electrical',
                'description': 'Engine management sensors, O2 sensors, MAF sensors, ignition coils, and ECU relays.',
                'icon_class': 'fas fa-microchip'
            },
            {
                'name': 'Wiring & Accessories',
                'description': 'Professional automotive wires, fuse blocks, switches, relays, and custom harness kits.',
                'icon_class': 'fas fa-plug'
            },
            {
                'name': 'Lighting Systems',
                'description': 'High-performance LED conversions, xenon bulbs, flashers, and auxiliary light bars.',
                'icon_class': 'fas fa-lightbulb'
            }
        ]
        
        categories = {}
        for cat_info in categories_data:
            cat = Category.objects.create(
                name=cat_info['name'],
                description=cat_info['description'],
                icon_class=cat_info['icon_class']
            )
            categories[cat.name] = cat
            
        # 3. Parts table is intentionally left empty so the business owner can populate real inventory.
        self.stdout.write("Parts table initialized clean (0 dummy parts). Ready for owner stock management.")
            
        # 4. Create Company Profile
        CompanyProfile.objects.create(
            name='Jazz Auto Electrics',
            slogan='Where Precision Meets Harmony',
            phone='+263 71 294 8625',
            phone_raw='+263712948625',
            alt_phone='+263 77 425 5065',
            alt_phone_raw='+263774255065',
            whatsapp='+263 71 294 8625',
            whatsapp_url='https://wa.me/263712948625?text=Hi%20Jazz%20Auto%20Electrics,%20I%20would%20like%20to%20inquire%20about%20your%20services%20or%20motor%20spares.',
            facebook_url='https://www.facebook.com/profile.php?id=100064758844406',
            instagram_url='https://www.instagram.com/jazz_auto_electrics/',
            tiktok_url='https://www.tiktok.com/@jazzauto_electrics',
            email='info@jazzautoelectrics.co.zw',
            address='Cold Comfort, Harare, Zimbabwe (Mobile Workshop Nationwide)',
            hours_weekdays='Mon - Fri: 8:00 AM - 5:00 PM',
            hours_saturday='Sat: 8:00 AM - 1:00 PM',
            hours_sunday='Sun: Closed',
            map_latitude=-17.8228,
            map_longitude=30.9856,
            hero_tag='DEALER-LEVEL DIAGNOSTICS & HYBRID SPECIALISTS',
            hero_title='Dealer-Level Diagnostics & High-Precision Auto Electrics',
            hero_subtitle="Equipped with dealer-level diagnostic scanners & high-precision testing equipment. We specialize in Toyota hybrid high voltage battery servicing & cell replacement, Honda GP dual clutch replacements, and high-precision electrical repairs.",
            status_diagnostics_queue='Active (Cold Comfort & Mobile Workshop)',
            status_diagnostics_class='val-green',
            status_location_text='Cold Comfort, Harare'
        )

        # 5. Create Services
        services_data = [
            {
                'title': 'Computer & Dealer-Level Diagnostic Testing',
                'slug': 'diagnostics',
                'icon_class': 'fas fa-laptop-code',
                'description': 'Equipped with dealer-level diagnostics scanners and high-precision testing equipment. We perform factory-level ECU scans, sensor signal monitoring, wiring circuit analysis, and live telemetry tracking to accurately resolve complex electrical issues.',
                'bullet_points': (
                    "fas fa-laptop-code | Dealer-Level Diagnostics Scanners & Scopes\n"
                    "fas fa-microchip | Full Fault Code Scan & Reset\n"
                    "fas fa-tachometer-alt | Sensor Live Data & High-Precision Diagnostics\n"
                    "fas fa-sliders-h | Adaptations & ECU Module Coding"
                ),
                'order': 1
            },
            {
                'title': 'Toyota Hybrid High Voltage (HV) Battery Servicing',
                'slug': 'hybrid_battery',
                'icon_class': 'fas fa-car-battery',
                'description': 'Comprehensive battery diagnosis & replacement of all Toyota hybrid high voltage batteries (Prius, Aqua, Axio, Fielder, Camry, Harrier). We perform battery balancing & voltage analysis, and replace weak high voltage cells to restore peak battery efficiency.',
                'bullet_points': (
                    "fas fa-car-battery | Battery Diagnosis & Replacement of All Toyota Hybrids\n"
                    "fas fa-balance-scale | Battery Balancing & Individual Voltage Analysis\n"
                    "fas fa-tools | Individual Weak High Voltage Cell Replacement\n"
                    "fas fa-bolt | Full High Voltage (HV) Pack Refurbishment & Swap"
                ),
                'order': 2
            },
            {
                'title': 'Honda GP Dual Clutch Replacement & Servicing',
                'slug': 'dual_clutch',
                'icon_class': 'fas fa-cogs',
                'description': "All Honda GP models (Fit GP1, GP4, GP5, Vezel, Grace, Shuttle, Freed, etc.) need good care. We do full service of the dual clutch, and when failed, we replace it with a brand new clutch & release bearing along with actuator fluid servicing & calibration.",
                'bullet_points': (
                    "fas fa-cog | Complete Dual Clutch Service & Maintenance\n"
                    "fas fa-shield-alt | Brand New Clutch & Bearing Replacement\n"
                    "fas fa-oil-can | Dual Clutch Actuator Fluid Service & Bleeding\n"
                    "fas fa-sliders-h | Clutch Point Re-learning & Software Adaptations"
                ),
                'order': 3
            },
            {
                'title': 'Electrical Repairs & Wiring Harnesses',
                'slug': 'electrical_repairs',
                'icon_class': 'fas fa-tools',
                'description': 'From repairing frayed wire harnesses, splicing corroded connectors, and installing upgraded fuse boards, to resolving short circuits and fixing window regulators/door lock actuators. We repair electrical systems to factory standards.',
                'bullet_points': (
                    "fas fa-fire-extinguisher | Short Circuit Repair\n"
                    "fas fa-plug | Wiring Harness Splicing & Re-pinning\n"
                    "fas fa-lock | Central Locking & Power Window Repair\n"
                    "fas fa-fan | AC Blower & Radiator Fan Electricals"
                ),
                'order': 4
            },
            {
                'title': 'Alternator & Starter Repairs',
                'slug': 'alternator_starter',
                'icon_class': 'fas fa-sync-alt',
                'description': 'Starting problems or battery warnings are often down to the starter motor or alternator. We rebuild your starter or alternator in-house, replacing worn carbon brushes, diodes, voltage regulators, internal bearings, and solenoid relays to save you money.',
                'bullet_points': (
                    "fas fa-cog | Starter Solenoid Replacement\n"
                    "fas fa-atom | Alternator Diode Plate & Brush Rebuilds\n"
                    "fas fa-signal | Voltage Regulator Replacements\n"
                    "fas fa-shield-virus | Heavy Duty Truck Starter Servicing"
                ),
                'order': 5
            },
            {
                'title': 'General Auto-Electrical Troubleshooting',
                'slug': 'troubleshooting',
                'icon_class': 'fas fa-search',
                'description': "Whether it's a dashboard screen flickering, radio cutting out, alarms sounding randomly, or ABS/Airbag warnings illuminating, our auto-electrics engineers have the troubleshooting skills and schematics to track down the root cause.",
                'bullet_points': (
                    "fas fa-exclamation-triangle | ABS, SRS (Airbag) Fault Repair\n"
                    "fas fa-tv | Instrument Cluster & Screen Fixes\n"
                    "fas fa-bell-slash | Car Alarm & Immobilizer Troubleshooting\n"
                    "fas fa-trailer | Trailer Socket & Towbar Wiring"
                ),
                'order': 6
            }
        ]

        for s_info in services_data:
            Service.objects.create(
                title=s_info['title'],
                slug=s_info['slug'],
                icon_class=s_info['icon_class'],
                description=s_info['description'],
                bullet_points=s_info['bullet_points'],
                order=s_info['order']
            )

        # 6. Create Testimonials
        testimonials_data = [
            {
                'name': 'Tinashe M.',
                'role': 'Harare Driver',
                'rating': 5,
                'text': "My Toyota Hilux had a complex battery draining issue that two workshops couldn't fix. The guys at Jazz Auto Electric diagnosed it as a faulty alternator regulator within an hour. Professional and very fast!",
                'is_active': True
            },
            {
                'name': 'Sarah G.',
                'role': 'SUV Owner',
                'rating': 5,
                'text': "Awesome shop! Finding quality LED wiring harnesses and relay kits in Harare is usually a headache. Jazz had exactly what I needed in stock at a reasonable price in USD. Highly recommended.",
                'is_active': True
            },
            {
                'name': 'Farai Z.',
                'role': 'Fleet Manager',
                'rating': 5,
                'text': "I had my starter motor rebuilt here. They gave me a 6-month warranty and the car fires up instantly now. Excellent service, clean workshop, and very transparent pricing.",
                'is_active': True
            }
        ]

        for t_info in testimonials_data:
            Testimonial.objects.create(
                name=t_info['name'],
                role=t_info['role'],
                rating=t_info['rating'],
                text=t_info['text'],
                is_active=t_info['is_active']
            )

        # 7. Create Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@jazzautoelectric.co.zw', 'admin1234')
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' with password 'admin1234' created successfully."))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(categories)} categories, 0 initial parts (ready for owner inventory), 6 services, and 3 testimonials.'))
