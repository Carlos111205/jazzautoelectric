/* ==========================================================================
   Jazz Auto Electric - Interactive Frontend Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    
    // ----------------------------------------------------------------------
    // 1. Navigation Scroll & Mobile Toggle Behavior
    // ----------------------------------------------------------------------
    const navbar = document.getElementById('navbar');
    const mobileToggle = document.getElementById('mobile-toggle');
    const navLinks = document.getElementById('nav-links');

    // Add scroll class for navbar styling
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle click handler
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', function() {
            navLinks.classList.toggle('open');
            // Toggle icon representation
            const icon = mobileToggle.querySelector('i');
            if (navLinks.classList.contains('open')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });
    }

    // Close menu when clicking any nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (navLinks) navLinks.classList.remove('open');
            if (mobileToggle) {
                const icon = mobileToggle.querySelector('i');
                if (icon) icon.className = 'fas fa-bars';
            }
        });
    });

    // ----------------------------------------------------------------------
    // 2. Booking Pre-fill Hooks (from Service Cards)
    // ----------------------------------------------------------------------
    const serviceButtons = document.querySelectorAll('.select-booking-service');
    const serviceDropdown = document.querySelector('select[name="service_type"]');
    const bookingSection = document.getElementById('booking-section');

    serviceButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const serviceVal = this.getAttribute('data-service');
            if (serviceDropdown && serviceVal) {
                serviceDropdown.value = serviceVal;
            }
            if (bookingSection) {
                bookingSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // ----------------------------------------------------------------------
    // 3. Interactive Symptom Diagnosis Assistant
    // ----------------------------------------------------------------------
    const checkboxes = document.querySelectorAll('.symptom-checkbox');
    const resultBox = document.getElementById('diagnosis-result-box');
    const emptyState = resultBox ? resultBox.querySelector('.empty-state') : null;
    const reportDiv = resultBox ? resultBox.querySelector('.diagnosis-report') : null;
    const prefillBtn = document.getElementById('prefill-booking-btn');

    let lastCalculatedService = 'diagnostics';
    let lastCalculatedSymptomsText = '';

    if (checkboxes.length > 0 && resultBox) {
        checkboxes.forEach(cb => {
            cb.addEventListener('change', calculateDiagnosis);
        });
    }

    function calculateDiagnosis() {
        // Collect checked symptoms
        const checked = Array.from(checkboxes).filter(c => c.checked);
        
        if (checked.length === 0) {
            emptyState.style.display = 'block';
            reportDiv.style.display = 'none';
            resultBox.classList.remove('active-result');
            return;
        }

        // Active State
        emptyState.style.display = 'none';
        reportDiv.style.display = 'flex';
        resultBox.classList.add('active-result');

        const values = checked.map(c => c.value);
        const titles = checked.map(c => c.getAttribute('data-title'));
        
        let issues = '';
        let steps = [];
        let serviceKey = 'diagnostics';
        let serviceName = 'Diagnostic Testing';

        // Core symptoms rule engine
        if (values.includes('no-crank')) {
            issues = 'Faulty starter motor solenoid, complete battery failure, or ignition switch circuit break.';
            steps = [
                'Load test vehicle battery to check under-load cranking voltage.',
                'Inspect starter motor wire connections for corroded terminals.',
                'Test starter motor relay contacts and ignition fuse.'
            ];
            serviceKey = 'alternator_starter';
            serviceName = 'Alternator/Starter Repairs';
        } 
        else if (values.includes('warning-light') || (values.includes('dim-lights') && values.includes('draining'))) {
            issues = 'Alternator charging failure or faulty voltage regulator (battery is not receiving charge).';
            steps = [
                'Measure charging system output using digital multimeter (should read 13.8V-14.4V).',
                'Inspect alternator belt tension and pulley integrity.',
                'Check alternator harness connections.'
            ];
            serviceKey = 'alternator_starter';
            serviceName = 'Alternator/Starter Repairs';
        }
        else if (values.includes('draining')) {
            issues = 'Parasitic battery current drain or degraded battery cells.';
            steps = [
                'Perform battery health and capacity test.',
                'Perform parasitic draw milliamp test on fuse board (locating sleeping current leak).',
                'Verify alternator charging voltage output.'
            ];
            serviceKey = 'battery_replacement';
            serviceName = 'Battery Replacement';
        }
        else if (values.includes('blown-fuses')) {
            issues = 'Active short circuit in vehicle power wiring lines.';
            steps = [
                'Inspect circuit fuse logs to identify specific component groups.',
                'Trace wire lines using audio circuit signal tracer to locate chassis shorts.',
                'Inspect harness grommets passing through bulkhead firewall.'
            ];
            serviceKey = 'electrical_repairs';
            serviceName = 'Electrical Repairs';
        }
        else if (values.includes('accessories')) {
            issues = 'Actuator failure, broken ground connection, or body control module (BCM) signaling fault.';
            steps = [
                'Verify wiring harness ground points for corrosion.',
                'Check continuity of control switch circuits.',
                'Retrieve comfort and body electrical logs from BCM module.'
            ];
            serviceKey = 'troubleshooting';
            serviceName = 'General Auto-Electrical Troubleshooting';
        }
        else {
            issues = 'Intermittent auto-electrical fault or sensor signal distortion.';
            steps = [
                'Run full OBD2 diagnostic scan on vehicle ECUs.',
                'Verify sensor signal loops and ground pins.',
                'Check dashboard logs history.'
            ];
            serviceKey = 'diagnostics';
            serviceName = 'Diagnostic Testing';
        }

        // Store calculations globally to apply to booking form
        lastCalculatedService = serviceKey;
        lastCalculatedSymptomsText = `Symptoms Selected:\n` + titles.map(t => `- ${t}`).join('\n') + `\n\nInitial AI Diagnosis Suggestion:\n${issues}`;

        // Render to UI
        document.getElementById('diag-issues').textContent = issues;
        const stepsContainer = document.getElementById('diag-steps');
        stepsContainer.innerHTML = '';
        steps.forEach(step => {
            const li = document.createElement('li');
            li.textContent = step;
            stepsContainer.appendChild(li);
        });

        const serviceBadge = document.getElementById('diag-service-badge');
        serviceBadge.textContent = serviceName;
        // Dynamically style based on service type
        if (serviceKey === 'alternator_starter') {
            serviceBadge.style.borderColor = 'var(--color-accent-yellow)';
            serviceBadge.style.color = 'var(--color-accent-yellow)';
        } else {
            serviceBadge.style.borderColor = 'var(--color-accent-blue)';
            serviceBadge.style.color = 'var(--color-accent-blue)';
        }
    }

    // Prefill form action
    if (prefillBtn) {
        prefillBtn.addEventListener('click', function() {
            // Pre-select service dropdown
            if (serviceDropdown) {
                serviceDropdown.value = lastCalculatedService;
            }
            // Pre-fill symptom text area
            const symptomsTextArea = document.querySelector('textarea[name="message"]');
            if (symptomsTextArea) {
                symptomsTextArea.value = lastCalculatedSymptomsText;
            }
            // Scroll to form
            if (bookingSection) {
                bookingSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // ----------------------------------------------------------------------
    // 4. Shop Specifications Accordion Toggle
    // ----------------------------------------------------------------------
    const accordionButtons = document.querySelectorAll('.specs-toggle-btn');
    accordionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const chevron = this.querySelector('i');
            
            if (content.style.display === 'none') {
                content.style.display = 'block';
                chevron.className = 'fas fa-chevron-up';
                this.classList.add('active');
            } else {
                content.style.display = 'none';
                chevron.className = 'fas fa-chevron-down';
                this.classList.remove('active');
            }
        });
    });

    // ----------------------------------------------------------------------
    // 5. Instant Client-Side Search Filter (For instant feedback)
    // ----------------------------------------------------------------------
    const searchInput = document.getElementById('parts-search-input');
    const partCards = document.querySelectorAll('.part-card');
    const emptyShopState = document.querySelector('.empty-shop-state');

    if (searchInput && partCards.length > 0) {
        searchInput.addEventListener('input', function() {
            const term = this.value.toLowerCase().trim();
            let visibleCount = 0;

            partCards.forEach(card => {
                const name = card.getAttribute('data-name');
                const sku = card.getAttribute('data-sku');
                const desc = card.getAttribute('data-desc');

                if (name.includes(term) || sku.includes(term) || desc.includes(term)) {
                    card.style.display = 'flex';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            // Show empty state if nothing found client-side
            if (emptyShopState) {
                if (visibleCount === 0) {
                    emptyShopState.style.display = 'block';
                } else {
                    emptyShopState.style.display = 'none';
                }
            }
        });
    }

    // ----------------------------------------------------------------------
    // 6. Leaflet Map Setup (Dark themed CartoDB Tiles)
    // ----------------------------------------------------------------------
    const mapElement = document.getElementById('contact-map');
    if (mapElement && typeof L !== 'undefined') {
        
        // Coordinates: workshopLat, workshopLng must be loaded from window context (in contact.html)
        const lat = typeof workshopLat !== 'undefined' ? workshopLat : -17.8485;
        const lng = typeof workshopLng !== 'undefined' ? workshopLng : 31.0605;
        const name = typeof businessName !== 'undefined' ? businessName : 'Jazz Auto Electric';
        const address = typeof businessAddress !== 'undefined' ? businessAddress : 'Graniteside, Harare';

        // Initialize Map
        const map = L.map('contact-map', {
            center: [lat, lng],
            zoom: 15,
            scrollWheelZoom: false // disable scrolling zoom for better page scroll UX
        });

        // Add Dark Theme CartoDB Tile Layer
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        // Add a Marker with Popup info
        const marker = L.marker([lat, lng]).addTo(map);
        marker.bindPopup(`
            <div style="font-family: 'Inter', sans-serif;">
                <h4 style="margin: 0 0 5px 0; color: #f5b016; font-weight: 700;">${name}</h4>
                <p style="margin: 0; font-size: 0.85rem; color: #f1f5f9;">${address}</p>
            </div>
        `).openPopup();
    }

});
