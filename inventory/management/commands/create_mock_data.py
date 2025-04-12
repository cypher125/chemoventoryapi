from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import Users
from inventory.models import Locations, Chemicals, ChemicalActivity
import random
from datetime import timedelta


class Command(BaseCommand):
    help = "Create mock data for Chemoventry app including users, locations, chemicals, and activities"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting mock data creation..."))
        
        # Create users
        users = self.create_users()
        
        # Create locations
        locations = self.create_locations()
        
        # Create chemicals
        chemicals = self.create_chemicals(users, locations)
        
        # Create chemical activities
        self.create_chemical_activities(chemicals, users)
        
        self.stdout.write(self.style.SUCCESS("\nMock data creation complete!"))
        self.stdout.write(self.style.SUCCESS("\nCreated Users:"))
        self.stdout.write("- Admin 1: admin1@chemoventry.com (password: admin123)")
        self.stdout.write("- Admin 2: admin2@chemoventry.com (password: admin123)")
        self.stdout.write("- Lab Attendant: labtech@chemoventry.com (password: lab123)")

    def create_users(self):
        """Create 2 admin users and 1 lab attendant"""
        self.stdout.write("Creating users...")
        
        # Check if users already exist
        if Users.objects.filter(email__in=["admin1@chemoventry.com", "admin2@chemoventry.com", "labtech@chemoventry.com"]).exists():
            self.stdout.write(self.style.WARNING("Users already exist! Skipping user creation."))
            return Users.objects.all()
        
        # Create admin users
        admin1 = Users.objects.create_user(
            email="admin1@chemoventry.com",
            password="admin123",
            first_name="John",
            last_name="Admin",
            role="admin",
            is_staff=True,
            is_superuser=True
        )
        
        admin2 = Users.objects.create_user(
            email="admin2@chemoventry.com",
            password="admin123",
            first_name="Jane",
            last_name="Director",
            role="admin",
            is_staff=True,
            is_superuser=True
        )
        
        # Create lab attendant
        attendant = Users.objects.create_user(
            email="labtech@chemoventry.com",
            password="lab123",
            first_name="Alex",
            last_name="Technician",
            role="attendant",
            is_staff=False,
            is_superuser=False
        )
        
        self.stdout.write(self.style.SUCCESS(f"Created users: {admin1}, {admin2}, {attendant}"))
        return Users.objects.all()

    def create_locations(self):
        """Create sample lab locations"""
        self.stdout.write("Creating locations...")
        
        # Check if locations already exist
        if Locations.objects.exists():
            self.stdout.write(self.style.WARNING("Locations already exist! Skipping location creation."))
            return Locations.objects.all()
        
        locations = [
            Locations(name="Lab A - Main Storage"),
            Locations(name="Lab B - Organic Chemistry"),
            Locations(name="Storage Room 1"),
            Locations(name="Storage Room 2"),
            Locations(name="Cold Storage Unit"),
            Locations(name="Hazardous Materials Cabinet")
        ]
        
        Locations.objects.bulk_create(locations)
        self.stdout.write(self.style.SUCCESS(f"Created {len(locations)} locations"))
        return Locations.objects.all()

    def create_chemicals(self, users, locations):
        """Create sample chemicals across different locations"""
        self.stdout.write("Creating chemicals...")
        
        # Check if chemicals already exist
        if Chemicals.objects.exists():
            self.stdout.write(self.style.WARNING("Chemicals already exist! Skipping chemical creation."))
            return Chemicals.objects.all()
        
        chemical_data = [
            {
                "name": "Sodium Chloride",
                "quantity": 5000,
                "description": "Common table salt",
                "vendor": "Sigma-Aldrich",
                "hazard_information": "Low hazard",
                "molecular_formula": "NaCl",
                "reactivity_group": "Alkali",
                "chemical_type": "Inorganic",
                "chemical_state": "Solid",
                "expires": timezone.now().date() + timedelta(days=365*2)  # 2 years
            },
            {
                "name": "Ethanol",
                "quantity": 2000,
                "description": "Pure ethanol for laboratory use",
                "vendor": "Merck",
                "hazard_information": "Flammable liquid",
                "molecular_formula": "C2H5OH",
                "reactivity_group": "Other",
                "chemical_type": "Organic",
                "chemical_state": "Liquid",
                "expires": timezone.now().date() + timedelta(days=365)  # 1 year
            },
            {
                "name": "Hydrochloric Acid",
                "quantity": 1500,
                "description": "Strong acid for various reactions",
                "vendor": "Fisher Scientific",
                "hazard_information": "Corrosive, causes severe burns",
                "molecular_formula": "HCl",
                "reactivity_group": "Nonmetal",
                "chemical_type": "Inorganic",
                "chemical_state": "Liquid",
                "expires": timezone.now().date() + timedelta(days=365)  # 1 year
            },
            {
                "name": "Sulfuric Acid",
                "quantity": 800,
                "description": "Strong acid used in many industrial applications",
                "vendor": "Fisher Scientific",
                "hazard_information": "Highly corrosive, causes severe burns and eye damage",
                "molecular_formula": "H2SO4",
                "reactivity_group": "Nonmetal",
                "chemical_type": "Inorganic",
                "chemical_state": "Liquid",
                "expires": timezone.now().date() + timedelta(days=730)  # 2 years
            },
            {
                "name": "Acetone",
                "quantity": 1200,
                "description": "Common solvent used in labs",
                "vendor": "Merck",
                "hazard_information": "Highly flammable, irritant",
                "molecular_formula": "C3H6O",
                "reactivity_group": "Other",
                "chemical_type": "Organic",
                "chemical_state": "Liquid",
                "expires": timezone.now().date() + timedelta(days=180)  # 6 months
            },
            {
                "name": "Sodium Hydroxide",
                "quantity": 500,
                "description": "Strong base used in various reactions",
                "vendor": "Sigma-Aldrich",
                "hazard_information": "Corrosive, causes severe burns",
                "molecular_formula": "NaOH",
                "reactivity_group": "Alkali",
                "chemical_type": "Inorganic",
                "chemical_state": "Solid",
                "expires": timezone.now().date() + timedelta(days=365)  # 1 year
            },
            {
                "name": "Methanol",
                "quantity": 750,
                "description": "Common lab solvent",
                "vendor": "Merck",
                "hazard_information": "Toxic, flammable",
                "molecular_formula": "CH3OH",
                "reactivity_group": "Other",
                "chemical_type": "Organic",
                "chemical_state": "Liquid",
                "expires": timezone.now().date() + timedelta(days=270)  # 9 months
            },
            {
                "name": "Potassium Permanganate",
                "quantity": 300,
                "description": "Oxidizing agent",
                "vendor": "Fisher Scientific",
                "hazard_information": "Oxidizer, harmful if swallowed",
                "molecular_formula": "KMnO4",
                "reactivity_group": "Transition Metal",
                "chemical_type": "Inorganic",
                "chemical_state": "Solid",
                "expires": timezone.now().date() + timedelta(days=540)  # 18 months
            },
            {
                "name": "Hydrogen Peroxide 30%",
                "quantity": 400,
                "description": "Strong oxidizer",
                "vendor": "Sigma-Aldrich",
                "hazard_information": "Oxidizer, causes burns",
                "molecular_formula": "H2O2",
                "reactivity_group": "Nonmetal",
                "chemical_type": "Inorganic",
                "chemical_state": "Liquid",
                "expires": timezone.now().date() + timedelta(days=90)  # 3 months
            },
            {
                "name": "Benzene",
                "quantity": 250,
                "description": "Aromatic hydrocarbon",
                "vendor": "Merck",
                "hazard_information": "Carcinogen, flammable",
                "molecular_formula": "C6H6",
                "reactivity_group": "Other",
                "chemical_type": "Organic",
                "chemical_state": "Liquid",
                "expires": timezone.now().date() + timedelta(days=365)  # 1 year
            },
            # Add a few chemicals that are expired or about to expire
            {
                "name": "Lithium Chloride",
                "quantity": 100,
                "description": "Salt used in various applications",
                "vendor": "Sigma-Aldrich",
                "hazard_information": "Harmful if swallowed",
                "molecular_formula": "LiCl",
                "reactivity_group": "Alkali",
                "chemical_type": "Inorganic",
                "chemical_state": "Solid",
                "expires": timezone.now().date() - timedelta(days=30)  # Expired 1 month ago
            },
            {
                "name": "Calcium Carbonate",
                "quantity": 75,
                "description": "Chalk/limestone compound",
                "vendor": "Fisher Scientific",
                "hazard_information": "Low hazard",
                "molecular_formula": "CaCO3",
                "reactivity_group": "Alkaline Earth",
                "chemical_type": "Inorganic",
                "chemical_state": "Solid",
                "expires": timezone.now().date() - timedelta(days=15)  # Expired 15 days ago
            },
            # Add a few chemicals with low stock
            {
                "name": "Ammonium Nitrate",
                "quantity": 50,
                "description": "Fertilizer and oxidizer",
                "vendor": "Merck",
                "hazard_information": "Oxidizer, may cause fire",
                "molecular_formula": "NH4NO3",
                "reactivity_group": "Other",
                "chemical_type": "Inorganic",
                "chemical_state": "Solid",
                "expires": timezone.now().date() + timedelta(days=180)  # 6 months
            },
            {
                "name": "Silver Nitrate",
                "quantity": 25,
                "description": "Used in analytical chemistry",
                "vendor": "Sigma-Aldrich",
                "hazard_information": "Corrosive, oxidizer",
                "molecular_formula": "AgNO3",
                "reactivity_group": "Transition Metal",
                "chemical_type": "Inorganic",
                "chemical_state": "Solid",
                "expires": timezone.now().date() + timedelta(days=365)  # 1 year
            },
        ]
        
        chemicals = []
        for chem_data in chemical_data:
            chemicals.append(Chemicals(
                **chem_data,
                location=random.choice(locations),
                created_by=random.choice(users)
            ))
        
        Chemicals.objects.bulk_create(chemicals)
        self.stdout.write(self.style.SUCCESS(f"Created {len(chemicals)} chemicals"))
        return Chemicals.objects.all()

    def create_chemical_activities(self, chemicals, users):
        """Create sample chemical activities"""
        self.stdout.write("Creating chemical activities...")
        
        # Check if activities already exist
        if ChemicalActivity.objects.count() > 10:  # Allow a few existing activities
            self.stdout.write(self.style.WARNING("Chemical activities already exist! Skipping activity creation."))
            return
        
        activities = []
        action_types = ['added', 'updated', 'removed', 'used', 'restocked']
        
        # Generate 50 random activities spread over the last 6 months
        for i in range(50):
            chemical = random.choice(chemicals)
            user = random.choice(users)
            action = random.choice(action_types)
            
            # Random time in the past 6 months
            days_ago = random.randint(0, 180)
            activity_time = timezone.now() - timedelta(days=days_ago)
            
            # Reasonable quantity changes based on action
            if action in ['added', 'restocked']:
                quantity = random.randint(10, 200)
            elif action in ['removed', 'used']:
                quantity = -random.randint(10, 100)
            else:  # updated
                quantity = chemical.quantity + random.randint(-50, 50)
                quantity = max(0, quantity)  # Ensure quantity doesn't go below 0
            
            activity = ChemicalActivity(
                chemical=chemical,
                action=action,
                quantity=quantity,
                user=user,
                timestamp=activity_time,
                notes=f"Mock {action} activity for testing"
            )
            activities.append(activity)
        
        # Sort by timestamp to ensure chronological order
        activities.sort(key=lambda x: x.timestamp)
        
        # Save one by one to trigger the custom save method
        for activity in activities:
            try:
                activity.save()
                # Adding a success message for first few activities for brevity
                if activities.index(activity) < 5:
                    self.stdout.write(f"Added activity: {activity}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating activity: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"Created {len(activities)} chemical activities"))
