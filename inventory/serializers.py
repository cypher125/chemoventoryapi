from rest_framework import serializers
from .models import Chemicals, Locations


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ['id', 'name']


class ChemicalListSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    unit = serializers.SerializerMethodField()

    class Meta:
        model = Chemicals
        fields = [
            'id',
            'name',
            'quantity',
            'unit',
            'molecular_formula',
            'reactivity_group',
            'chemical_type',
            'chemical_state',
            'location',
            'location_name',
            'expires'
        ]

    def get_unit(self, obj):
        return 'L' if obj.chemical_state == 'Liquid' else 'g'


class ChemicalSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    unit = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Chemicals
        fields = [
            'id',
            'name',
            'quantity',
            'unit',
            'description',
            'vendor',
            'hazard_information',
            'molecular_formula',
            'reactivity_group',
            'chemical_type',
            'chemical_state',
            'location',
            'location_name',
            'expires',
            'created_by',
            'created_by_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_unit(self, obj):
        return 'L' if obj.chemical_state == 'Liquid' else 'g'
