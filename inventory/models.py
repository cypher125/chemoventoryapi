from django.db import models
import uuid
from users.models import Users
from chemoventry import settings

class Locations(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=225, unique=True)

class Chemicals(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    quantity = models.FloatField(help_text="in gram(g) or liter(L)")
    description = models.TextField()
    vendor = models.CharField(max_length=100)
    hazard_information = models.TextField()
    molecular_formula = models.CharField(max_length=100)
    reactivity_group = models.CharField(max_length=255, choices=[
        ('Alkali', 'Alkali'),
        ('Alkaline Earth', 'Alkaline Earth'),
        ('Transition Metal', 'Transition Metal'),
        ('Lanthanide', 'Lanthanide'),
        ('Actinide', 'Actinide'),
        ('Metal', 'Metal'),
        ('Nonmetal', 'Nonmetal'),
        ('Halogen', 'Halogen'),
        ('Noble Gas', 'Noble Gas'),
        ('Other', 'Other'),
    ])
    chemical_type = models.CharField(max_length=100, choices=[
        ('Organic', 'Organic'),
        ('Inorganic', 'Inorganic'),
        ('Both', 'Both'),
    ])
    chemical_state = models.CharField(max_length=100, choices=[
        ('Solid', 'Solid'),
        ('Liquid', 'Liquid'),
        ('Gas', 'Gas'),
        ('Plasma', 'Plasma'),
        ('Other', 'Other'),
    ])
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='chemicals')
    expires = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_chemical')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['chemical_state']),
            models.Index(fields=['chemical_type']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['expires']),
        ]

    def __str__(self):
        return self.name

class ChemicalActivity(models.Model):
    ACTION_CHOICES = [
        ('added', 'Added'),
        ('updated', 'Updated'),
        ('removed', 'Removed'),
        ('used', 'Used'),
        ('restocked', 'Restocked'),
    ]

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    chemical = models.ForeignKey(Chemicals, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    quantity = models.FloatField(help_text="Change in quantity (positive for additions, negative for removals)")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chemical_activities')
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['action']),
            models.Index(fields=['chemical']),
            models.Index(fields=['user']),
        ]
        verbose_name_plural = 'Chemical Activities'

    def __str__(self):
        return f"{self.action} {self.chemical.name} by {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        # Update chemical quantity based on activity
        if self.action in ['added', 'restocked']:
            self.chemical.quantity += abs(self.quantity)
        elif self.action in ['removed', 'used']:
            self.chemical.quantity -= abs(self.quantity)
        elif self.action == 'updated':
            # For updates, quantity represents the new total
            self.chemical.quantity = self.quantity
        
        self.chemical.save()
        super().save(*args, **kwargs)