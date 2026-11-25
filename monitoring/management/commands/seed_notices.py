from decimal import Decimal
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from monitoring.models import Location, OfficialNotice


class Command(BaseCommand):
    help = "Seeds sample official heat notices and bulletins."

    def handle(self, *args, **options):
        # Retrieve or create an authority user
        staff_user = User.objects.filter(is_staff=True).first()
        if not staff_user:
            staff_user, _ = User.objects.get_or_create(
                username='staffuser',
                defaults={'is_staff': True}
            )

        now = timezone.now()
        locations = Location.objects.all()
        if not locations.exists():
            self.stdout.write(self.style.WARNING("No locations found. Run 'python manage.py seed_stations' first."))
            return

        delhi = locations.filter(name__icontains='Delhi').first() or locations.first()
        prayagraj = locations.filter(name__icontains='Prayagraj').first() or locations[1 if locations.count() > 1 else 0]
        guwahati = locations.filter(name__icontains='Guwahati').first() or locations.last()

        notices_data = [
            {
                "location": delhi,
                "title": "Severe Heatwave Warning - Orange Alert Issued",
                "message": (
                    "Maximum temperatures are very likely to exceed 43°C across the National Capital Region. "
                    "High risk of heat cramps and exhaustion during prolonged outdoor activity. "
                    "Public advised to avoid direct sunlight exposure between 12:00 PM and 3:30 PM, drink plenty of fluids, "
                    "and protect vulnerable populations including seniors, outdoor laborers, and children."
                ),
                "severity": "WARNING",
                "issuing_organization": "India Meteorological Department (IMD)",
                "source_url": "https://mausam.imd.gov.in/",
                "valid_from": now - timedelta(hours=2),
                "valid_until": now + timedelta(days=2),
                "is_published": True,
            },
            {
                "location": prayagraj,
                "title": "Heatwave Watch & Public Hydration Advisory",
                "message": (
                    "Persistently high thermal stress and elevated humidity expected along the Ganges plains. "
                    "Ensure adequate hydration and electrolyte balance. Shaded rest stations and water kiosks "
                    "have been established at major transit junctions."
                ),
                "severity": "WATCH",
                "issuing_organization": "State Disaster Management Authority (SDMA)",
                "source_url": "https://upsdma.up.nic.in/",
                "valid_from": now - timedelta(hours=5),
                "valid_until": now + timedelta(days=1),
                "is_published": True,
            },
            {
                "location": guwahati,
                "title": "Humid Thermal Stress Advisory - Brahmaputra Valley",
                "message": (
                    "High humidity coupled with daytime peak temperatures of 35-37°C creates high apparent heat indices. "
                    "Maintain proper indoor ventilation, wear light cotton clothing, and report early symptoms of dizziness or nausea."
                ),
                "severity": "ADVISORY",
                "issuing_organization": "Regional Meteorological Centre Guwahati",
                "source_url": "https://mausam.imd.gov.in/guwahati/",
                "valid_from": now - timedelta(hours=1),
                "valid_until": now + timedelta(days=3),
                "is_published": True,
            },
        ]

        count = 0
        for item in notices_data:
            notice, created = OfficialNotice.objects.get_or_create(
                location=item["location"],
                title=item["title"],
                defaults={
                    "message": item["message"],
                    "severity": item["severity"],
                    "issuing_organization": item["issuing_organization"],
                    "source_url": item["source_url"],
                    "valid_from": item["valid_from"],
                    "valid_until": item["valid_until"],
                    "created_by": staff_user,
                    "is_published": True,
                }
            )
            if created:
                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded {count} official notices (total {OfficialNotice.objects.count()} in database)."
            )
        )
