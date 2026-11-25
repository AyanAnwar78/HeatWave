from decimal import Decimal
from django.core.management.base import BaseCommand
from monitoring.models import Location


DEFAULT_STATIONS = [
    {
        "name": "Prayagraj",
        "state_or_region": "Uttar Pradesh",
        "country": "India",
        "latitude": Decimal("25.43580"),
        "longitude": Decimal("81.84630"),
    },
    {
        "name": "Delhi",
        "state_or_region": "Delhi",
        "country": "India",
        "latitude": Decimal("28.61390"),
        "longitude": Decimal("77.20900"),
    },
    {
        "name": "Mumbai",
        "state_or_region": "Maharashtra",
        "country": "India",
        "latitude": Decimal("19.07600"),
        "longitude": Decimal("72.87770"),
    },
    {
        "name": "Kolkata",
        "state_or_region": "West Bengal",
        "country": "India",
        "latitude": Decimal("22.57260"),
        "longitude": Decimal("88.36390"),
    },
    {
        "name": "Chennai",
        "state_or_region": "Tamil Nadu",
        "country": "India",
        "latitude": Decimal("13.08270"),
        "longitude": Decimal("80.27070"),
    },
    {
        "name": "Bengaluru",
        "state_or_region": "Karnataka",
        "country": "India",
        "latitude": Decimal("12.97160"),
        "longitude": Decimal("77.59460"),
    },
    {
        "name": "Hyderabad",
        "state_or_region": "Telangana",
        "country": "India",
        "latitude": Decimal("17.38500"),
        "longitude": Decimal("78.48670"),
    },
    {
        "name": "Ahmedabad",
        "state_or_region": "Gujarat",
        "country": "India",
        "latitude": Decimal("23.02250"),
        "longitude": Decimal("72.57140"),
    },
    {
        "name": "Jaipur",
        "state_or_region": "Rajasthan",
        "country": "India",
        "latitude": Decimal("26.91240"),
        "longitude": Decimal("75.78730"),
    },
    {
        "name": "Lucknow",
        "state_or_region": "Uttar Pradesh",
        "country": "India",
        "latitude": Decimal("26.84670"),
        "longitude": Decimal("80.94620"),
    },
    {
        "name": "Phagwara",
        "state_or_region": "Punjab",
        "country": "India",
        "latitude": Decimal("31.22400"),
        "longitude": Decimal("75.77080"),
    },
    {
        "name": "Patna",
        "state_or_region": "Bihar",
        "country": "India",
        "latitude": Decimal("25.59410"),
        "longitude": Decimal("85.13760"),
    },
]


class Command(BaseCommand):
    help = "Seeds default active monitoring stations across India."

    def handle(self, *args, **options):
        created_count = 0
        for s in DEFAULT_STATIONS:
            obj, created = Location.objects.get_or_create(
                name=s["name"],
                state_or_region=s["state_or_region"],
                country=s["country"],
                defaults={
                    "latitude": s["latitude"],
                    "longitude": s["longitude"],
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded stations. Created {created_count} new stations (total {Location.objects.count()} in database)."
            )
        )
