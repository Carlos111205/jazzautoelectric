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
        categories_data = [
            {
                'name': 'Batteries & Charging',
                'description': 'Premium automotive batteries, terminals, testers, and battery management components.',
                'icon_class': 'fas fa-car-battery'
            },
            {
                'name': 'Lighting Systems',
                'description': 'High-performance LED conversions, bulbs, relays, and complete wiring assemblies.',
                'icon_class': 'fas fa-lightbulb'
            },
            {
                'name': 'Sensors & Engine Electrical',
                'description': 'Engine management sensors, ABS sensors, spark plugs, ignition coils, and oxygen sensors.',
                'icon_class': 'fas fa-microchip'
            },
            {
                'name': 'Starters & Alternators',
                'description': 'Heavy-duty starter motors, alternators, regulators, solenoids, and repair components.',
                'icon_class': 'fas fa-sync-alt'
            },
            {
                'name': 'Wiring & Accessories',
                'description': 'Professional grade automotive wires, fuses, connectors, terminal blocks, and switches.',
                'icon_class': 'fas fa-plug'
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
            
        # 3. Create Parts
        parts_data = [
            # Batteries & Charging
            {
                'name': 'Exide Premium AGM Battery 12V 70Ah',
                'category': 'Batteries & Charging',
                'sku': 'EX-AGM-70',
                'description': 'Heavy-duty Absorbent Glass Mat (AGM) battery, ideal for modern vehicles with start-stop technology and high electrical demands.',
                'price': 145.00,
                'specifications': 'Voltage: 12V\nCapacity: 70 Ah\nCCA: 760 A\nTechnology: AGM\nDimensions: 278 x 175 x 190 mm\nWarranty: 12 Months'
            },
            {
                'name': 'Heavy-Duty Brass Battery Terminals (Pair)',
                'category': 'Batteries & Charging',
                'sku': 'BT-BR-HD',
                'description': 'Solid brass battery terminal clamps (positive and negative). Provides maximum conductivity and corrosion resistance for high-current auto-electrical connections.',
                'price': 12.50,
                'specifications': 'Material: Solid Brass\nPolarity: Positive (+) & Negative (-)\nConnection: Bolt-on\nCompatibility: Standard post batteries'
            },
            {
                'name': 'Digital Battery and Alternator Tester',
                'category': 'Batteries & Charging',
                'sku': 'BT-DIG-100',
                'description': 'Handheld 12V digital battery analyzer. Quickly tests battery health, cold cranking amps (CCA), and charging system/alternator output.',
                'price': 45.00,
                'specifications': 'Compatibility: 12V Batteries\nTest Range: 100 - 2000 CCA\nDisplay: Backlit LCD screen\nLanguage: English\nPower: Powered by vehicle battery'
            },
            
            # Lighting Systems
            {
                'name': 'H4 LED Headlight Conversion Kit 6000K',
                'category': 'Lighting Systems',
                'sku': 'LT-LED-H4',
                'description': 'Ultra-bright H4 LED headlight bulbs featuring advanced CSP chips. Delivers a clean 6000K cool white light with a perfect beam pattern and high-speed cooling fan.',
                'price': 38.00,
                'specifications': 'Bulb Type: H4 (High/Low Beam)\nBrightness: 12,000 LM per pair\nColor Temp: 6000K Cool White\nWattage: 50W per bulb\nLifespan: >30,000 hours\nWaterproof: IP67'
            },
            {
                'name': '4-Pin 12V 40A Waterproof Relay with Harness',
                'category': 'Lighting Systems',
                'sku': 'RL-WP-40A',
                'description': 'Professional-grade automotive relay with pre-wired socket harness. Sealed waterproof design, ideal for wiring auxiliary driving lights, horn, and fuel pumps.',
                'price': 8.99,
                'specifications': 'Voltage: 12V DC\nRating: 40 Amps\nPin Count: 4-Pin\nWire Gauge: 12 AWG (Power), 16 AWG (Trigger)\nHarness Length: 15 cm'
            },
            {
                'name': 'Universal 12-LED Slim Amber Strobe Light Bar',
                'category': 'Lighting Systems',
                'sku': 'LT-STRB-12A',
                'description': 'High-intensity amber warning strobe light. Slim profile design for grille or surface mount. Features 18 selectable flash patterns with pattern memory.',
                'price': 22.00,
                'specifications': 'Voltage: 12V - 24V DC\nLED Count: 12 High-Power LEDs\nColor: Amber\nPatterns: 18 flash modes\nWiring: 3-wire connection (Red, Black, Yellow)'
            },
            
            # Sensors & Engine Electrical
            {
                'name': 'Bosch Universal 4-Wire Oxygen (O2) Sensor',
                'category': 'Sensors & Engine Electrical',
                'sku': 'SN-BOS-O2',
                'description': 'Premium replacement heated oxygen sensor. Restores engine efficiency, reduces emissions, and improves fuel economy. Built with patented planar technology.',
                'price': 65.00,
                'specifications': 'Sensor Type: Heated (4-wire)\nThread Size: M18 x 1.5\nWire Length: 30 cm\nInstallation: Universal splicing kit included\nOEM Compatibility: Replaces standard 4-wire sensors'
            },
            {
                'name': 'Universal Ignition Coil Pack 12V',
                'category': 'Sensors & Engine Electrical',
                'sku': 'CO-UNIV-12V',
                'description': 'High-output ignition coil designed to deliver reliable sparks under high-performance conditions. Direct fit replacement for multiple passenger vehicle brands.',
                'price': 42.50,
                'specifications': 'Primary Resistance: 0.7 Ohms\nSecondary Resistance: 12k Ohms\nMax Voltage: 40,000V\nTerminal Type: HEI post\nMounting Bracket: Included'
            },
            
            # Starters & Alternators
            {
                'name': '12V 90A High Output Universal Alternator',
                'category': 'Starters & Alternators',
                'sku': 'AL-UNIV-90A',
                'description': 'Brand new high-output alternator suitable for various petrol and diesel engines. Built with heavy-duty bearings and premium internal copper windings to ensure stable voltage output.',
                'price': 135.00,
                'specifications': 'Voltage: 12V\nOutput: 90 Amps\nMounting Type: Spool (Universal)\nPulley Type: 1-Groove V-belt\nRegulator: Internal electronic'
            },
            {
                'name': 'Starter Motor Solenoid Switch 12V',
                'category': 'Starters & Alternators',
                'sku': 'ST-SOL-12V',
                'description': 'Heavy-duty starter solenoid. Solves common "click-only" starter problems. Designed to handle high-current starting loads without contact pitting.',
                'price': 19.50,
                'specifications': 'Voltage: 12V\nTerminal Thread: M8 Copper\nMounting: 2-bolt base flange\nDuty Cycle: Intermittent'
            },
            
            # Wiring & Accessories
            {
                'name': 'Premium 100ft Roll 14 AWG Automotive Wire',
                'category': 'Wiring & Accessories',
                'sku': 'WR-14AWG-BK',
                'description': 'High-quality copper conductor wire with oil, acid, and heat resistant PVC insulation. Perfect for dashboard wiring, lighting kits, and light accessories.',
                'price': 28.00,
                'specifications': 'Gauge: 14 AWG\nConductor: Stranded Copper\nLength: 100 feet (30.4m)\nColor: Black\nMax Temp: 105 degrees Celsius\nMax Voltage: 60V DC'
            },
            {
                'name': '6-Way Fuse Block Box with LED Warning Indicator',
                'category': 'Wiring & Accessories',
                'sku': 'FB-6W-LED',
                'description': 'Compact blade fuse panel with a clear plastic cover. Red LED warning light glows instantly when a fuse blows, allowing rapid troubleshooting.',
                'price': 18.50,
                'specifications': 'Input Rating: 100A Max\nOutput Rating: 30A Max per circuit\nFuse Type: Standard ATC/ATO blade\nIndicator: Red LED\nMaterial: PBT Base, Polycarbonate Cover'
            }
        ]
        
        for part_info in parts_data:
            cat = categories[part_info['category']]
            Part.objects.create(
                name=part_info['name'],
                category=cat,
                sku=part_info['sku'],
                description=part_info['description'],
                price=part_info['price'],
                specifications=part_info['specifications'],
                is_available=True
            )
            
        # 4. Create Company Profile
        CompanyProfile.objects.create(
            name='Jazz Auto Electric',
            phone='+263 77 245 6789',
            phone_raw='+263772456789',
            whatsapp='+263 77 245 6789',
            whatsapp_url='https://wa.me/263772456789?text=Hi%20Jazz%20Auto%20Electric,%20I%20would%20like%20to%20inquire%20about%20your%20services%20or%20motor%20spares.',
            email='info@jazzautoelectric.co.zw',
            address='Plot 104, Cripps Road, Graniteside, Harare, Zimbabwe',
            hours_weekdays='Mon - Fri: 8:00 AM - 5:00 PM',
            hours_saturday='Sat: 8:00 AM - 1:00 PM',
            hours_sunday='Sun: Closed',
            map_latitude=-17.8485,
            map_longitude=31.0605
        )

        # 5. Create Services
        services_data = [
            {
                'title': 'Computer Diagnostic Testing',
                'slug': 'diagnostics',
                'icon_class': 'fas fa-laptop-code',
                'description': 'Modern vehicles are computers on wheels. We perform factory-level ECU scans, sensor signal monitoring, wiring circuit analysis, and live telemetry tracking to identify exactly what is causing check-engine lights or mysterious electrical errors.',
                'bullet_points': (
                    "fas fa-microchip | Full Fault Code Scan & Reset\n"
                    "fas fa-tachometer-alt | Sensor Live Data Diagnostics\n"
                    "fas fa-network-wired | CAN-Bus Network Troubleshooting\n"
                    "fas fa-sliders-h | Adaptations & ECU Coding"
                ),
                'order': 1
            },
            {
                'title': 'Electrical Repairs',
                'slug': 'electrical_repairs',
                'icon_class': 'fas fa-tools',
                'description': 'From repairing frayed wire harnesses, splicing corroded connectors, and installing upgraded fuse boards, to resolving short circuits and fixing window regulators/door lock actuators. We repair electrical systems to factory standards.',
                'bullet_points': (
                    "fas fa-fire-extinguisher | Short Circuit Repair\n"
                    "fas fa-plug | Wiring Harness Splicing & Re-pinning\n"
                    "fas fa-lock | Central Locking & Power Window Repair\n"
                    "fas fa-fan | AC Blower & Radiator Fan Electricals"
                ),
                'order': 2
            },
            {
                'title': 'Battery Diagnostics & Replacement',
                'slug': 'battery_replacement',
                'icon_class': 'fas fa-car-battery',
                'description': "A dead battery isn't always just a bad battery—it could be a parasitic draw or a weak alternator. We test your battery health and the alternator's charging voltage. If you need a replacement, we supply and register high-performance AGM or Maintenance-Free batteries.",
                'bullet_points': (
                    "fas fa-bolt | CCA Load Testing & Health Check\n"
                    "fas fa-search-minus | Parasitic Current Leak Test\n"
                    "fas fa-sync | AGM & Start-Stop Battery Setup\n"
                    "fas fa-shield-alt | Battery Terminal Reconditioning"
                ),
                'order': 3
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
                'order': 4
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
                'order': 5
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

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(categories)} categories, {len(parts_data)} parts, 5 services, and 3 testimonials.'))
