#!/usr/bin/env python
"""
Script to populate the Chemoventry database with mock data.
This includes:
- 2 admin users
- 1 lab attendant user
- Multiple locations
- Multiple chemicals with varied properties
- Chemical activity records
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemoventry.settings')
django.setup()

from django.utils import timezone
from users.models import Users
from inventory.models import Locations, Chemicals, ChemicalActivity

def create_users():
    """Create 2 admin users and 1 lab attendant"""
    print("Creating users...")
    
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
    
    print(f"Created users: {admin1}, {admin2}, {attendant}")
    return [admin1, admin2, attendant]

def create_locations():
    """Create sample lab locations"""
    print("Creating locations...")
    locations = [
        Locations(name="Lab A - Main Storage"),
        Locations(name="Lab B - Organic Chemistry"),
        Locations(name="Storage Room 1"),
        Locations(name="Storage Room 2"),
        Locations(name="Cold Storage Unit"),
        Locations(name="Hazardous Materials Cabinet")
    ]
    
    Locations.objects.bulk_create(locations)
    print(f"Created {len(locations)} locations")
    return Locations.objects.all()

def create_chemicals(users, locations):
    """Create sample chemicals across different locations"""
    print("Creating chemicals...")
    
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
    print(f"Created {len(chemicals)} chemicals")
    return Chemicals.objects.all()

def create_chemical_activities(chemicals, users):
    """Create sample chemical activities"""
    print("Creating chemical activities...")
    
    activities = []
    action_types = ['added', 'updated', 'removed', 'used', 'restocked']
    
    # Generate 50 random activities spread over the last 6 months
    for i in range(50):
        chemical = random.choice(chemicals)
        user = random.choice(users)
        action = random.choice(action_types)
        
        # Random time in the past 6 months
        days_ago = random.randint(0, 180)
        timestamp = timezone.now() - timedelta(days=days_ago)
        
        # Reasonable quantity changes based on action
        if action in ['added', 'restocked']:
            quantity = random.randint(10, 200)
        elif action in ['removed', 'used']:
            quantity = -random.randint(10, 100)
        else:  # updated
            quantity = chemical.quantity + random.randint(-50, 50)
            
        activity = ChemicalActivity(
            chemical=chemical,
            action=action,
            quantity=quantity,
            user=user,
            timestamp=timestamp,
            notes=f"Mock {action} activity for testing"
        )
        activities.append(activity)
    
    # Sort by timestamp to ensure chronological order
    activities.sort(key=lambda x: x.timestamp)
    
    # Need to save one by one to trigger the override save method
    for activity in activities:
        activity.save()
    
    print(f"Created {len(activities)} chemical activities")

def main():
    """Main function to create all mock data"""
    print("Starting mock data creation...")
    
    # Check if data already exists
    if Users.objects.filter(email__in=["admin1@chemoventry.com", "admin2@chemoventry.com", "labtech@chemoventry.com"]).exists():
        user_input = input("Mock users already exist. Do you want to proceed anyway? (y/n): ")
        if user_input.lower() != 'y':
            print("Aborting operation.")
            return
    
    # Create data
    users = create_users()
    locations = create_locations()
    chemicals = create_chemicals(users, locations)
    create_chemical_activities(chemicals, users)
    
    print("\nMock data creation complete!")
    print("\nCreated Users:")
    print("- Admin 1: admin1@chemoventry.com (password: admin123)")
    print("- Admin 2: admin2@chemoventry.com (password: admin123)")
    print("- Lab Attendant: labtech@chemoventry.com (password: lab123)")

if __name__ == "__main__":
    main()
