from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import Chemicals, Locations, ChemicalActivity
from .serializers import ChemicalSerializer, ChemicalListSerializer, LocationSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db.models import Q, Count, Sum, F
from django.utils import timezone
from datetime import timedelta
import random
from django.http import HttpResponse, HttpResponseRedirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import openpyxl
from openpyxl.styles import Font, PatternFill
from io import BytesIO

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Locations.objects.all()

    @extend_schema(
        tags=['Location'],
        description='List all Locations',
        responses={200: LocationSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        tags=['Location'],
        description='Create new Location',
        responses={201: LocationSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        tags=['Location'],
        description='Get Location details',
        responses={200: LocationSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        tags=['Location'],
        description='Update Location',
        responses={200: LocationSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        tags=['Location'],
        description='Delete Location',
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ChemicalFilter(filters.FilterSet):
    chemical_type = filters.ChoiceFilter(choices=Chemicals.chemical_type.field.choices)
    chemical_state = filters.ChoiceFilter(choices=Chemicals.chemical_state.field.choices)
    reactivity_group = filters.ChoiceFilter(choices=Chemicals.reactivity_group.field.choices)
    location = filters.UUIDFilter()
    expires_before = filters.DateFilter(field_name='expires', lookup_expr='lte')
    expires_after = filters.DateFilter(field_name='expires', lookup_expr='gte')
    search = filters.CharFilter(method='filter_search')

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(molecular_formula__icontains=value)
        )

    class Meta:
        model = Chemicals
        fields = ['chemical_type', 'chemical_state', 'reactivity_group', 'location']


class ChemicalViewSet(viewsets.ModelViewSet):
    queryset = Chemicals.objects.all()
    serializer_class = ChemicalSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ChemicalFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ChemicalListSerializer
        return ChemicalSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        tags=['Chemicals'],
        description='List all Chemicals',
        parameters=[
            OpenApiParameter('chemical_type', OpenApiTypes.STR, 
                enum=['Organic', 'Inorganic', 'Both']),
            OpenApiParameter('chemical_state', OpenApiTypes.STR, 
                enum=['Solid', 'Liquid', 'Gas', 'Plasma', 'Other']),
            OpenApiParameter('reactivity_group', OpenApiTypes.STR,
                enum=['Alkali', 'Alkaline Earth', 'Transition Metal', 'Lanthanide', 
                      'Actinide', 'Metal', 'Nonmetal', 'Halogen', 'Noble Gas', 'Other']),
            OpenApiParameter('location', OpenApiTypes.UUID),
            OpenApiParameter('expires_before', OpenApiTypes.DATE),
            OpenApiParameter('expires_after', OpenApiTypes.DATE),
            OpenApiParameter('search', OpenApiTypes.STR),
        ],
        responses={200: ChemicalListSerializer}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        tags=['Chemicals'],
        description='Create new Chemical',
        responses={201: ChemicalSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Chemicals'],
        description='Get Chemical details',
        responses={200: ChemicalSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Chemicals'],
        description='Update Chemical',
        responses={200: ChemicalSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Chemicals'],
        description='Delete Chemical',
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    tags=['Dashboard'],
    description='Get dashboard statistics',
    responses={200: {
        'type': 'object',
        'properties': {
            'total_chemicals': {'type': 'integer'},
            'total_locations': {'type': 'integer'},
            'expiring_soon': {'type': 'integer'},
            'low_quantity': {'type': 'integer'},
            'chemical_types': {
                'type': 'object',
                'properties': {
                    'Organic': {'type': 'integer'},
                    'Inorganic': {'type': 'integer'},
                    'Both': {'type': 'integer'}
                }
            },
            'chemical_states': {
                'type': 'object',
                'properties': {
                    'Solid': {'type': 'integer'},
                    'Liquid': {'type': 'integer'},
                    'Gas': {'type': 'integer'},
                    'Plasma': {'type': 'integer'},
                    'Other': {'type': 'integer'}
                }
            },
            'chemicals_by_location': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'location': {'type': 'string'},
                        'count': {'type': 'integer'}
                    }
                }
            }
        }
    }}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_overview(request):
    """
    Get an overview of the chemical inventory dashboard including:
    - Total number of chemicals
    - Total number of locations
    - Number of chemicals expiring soon
    - Number of chemicals with low quantity
    - Distribution of chemicals by type and state
    - Distribution of chemicals by location
    """
    # Get basic counts
    total_chemicals = Chemicals.objects.count()
    total_locations = Locations.objects.count()
    
    # Get expiring soon count (within next 30 days)
    thirty_days_from_now = timezone.now().date() + timedelta(days=30)
    expiring_soon = Chemicals.objects.filter(expires__lte=thirty_days_from_now).count()
    
    # Get low quantity count (less than 10% of max_quantity)
    low_quantity = Chemicals.objects.filter(
        current_quantity__lte=0.1 * F('max_quantity')
    ).count()
    
    # Get chemical types distribution
    chemical_types = Chemicals.objects.values('chemical_type').annotate(
        count=Count('id')
    )
    types_dict = {item['chemical_type']: item['count'] for item in chemical_types}
    
    # Get chemical states distribution
    chemical_states = Chemicals.objects.values('chemical_state').annotate(
        count=Count('id')
    )
    states_dict = {item['chemical_state']: item['count'] for item in chemical_states}
    
    # Get chemicals by location
    chemicals_by_location = Locations.objects.annotate(
        chemical_count=Count('chemicals')
    ).values('name', 'chemical_count')
    
    response_data = {
        'total_chemicals': total_chemicals,
        'total_locations': total_locations,
        'expiring_soon': expiring_soon,
        'low_quantity': low_quantity,
        'chemical_types': types_dict,
        'chemical_states': states_dict,
        'chemicals_by_location': [
            {'location': item['name'], 'count': item['chemical_count']}
            for item in chemicals_by_location
        ]
    }
    
    return Response(response_data)


@extend_schema(
    tags=['Dashboard'],
    description='Get dashboard overview statistics',
    responses={200: {
        'type': 'object',
        'properties': {
            'total_chemicals': {'type': 'integer'},
            'expired_chemicals': {'type': 'integer'},
            'low_stock_alerts': {'type': 'integer'},
            'monthly_usage': {'type': 'number', 'format': 'float'},
            'monthly_usage_change': {'type': 'number', 'format': 'float'},
            'recent_activity': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'action': {'type': 'string'},
                        'chemical': {'type': 'string'},
                        'quantity': {'type': 'string'},
                        'user': {'type': 'string'},
                        'timestamp': {'type': 'string', 'format': 'date-time'}
                    }
                }
            },
            'usage_trends': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'month': {'type': 'string'},
                        'usage': {'type': 'number'}
                    }
                }
            }
        }
    }}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_overview(request):
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    six_months_ago = today - timedelta(days=180)

    # Basic stats
    total_chemicals = Chemicals.objects.count()
    expired_chemicals = Chemicals.objects.filter(expires__lt=today).count()
    low_stock_alerts = Chemicals.objects.filter(quantity__lt=100).count()

    # Calculate monthly usage
    current_month_usage = ChemicalActivity.objects.filter(
        timestamp__gte=current_month_start,
        action__in=['used', 'removed']
    ).aggregate(total=Sum('quantity'))['total'] or 0

    last_month_usage = ChemicalActivity.objects.filter(
        timestamp__gte=last_month_start,
        timestamp__lt=current_month_start,
        action__in=['used', 'removed']
    ).aggregate(total=Sum('quantity'))['total'] or 0

    monthly_usage_change = ((current_month_usage - last_month_usage) / last_month_usage * 100) if last_month_usage > 0 else 0

    # Get recent activity
    recent_activity = ChemicalActivity.objects.select_related('chemical', 'user').order_by('-timestamp')[:5]
    activity_list = []
    
    for activity in recent_activity:
        quantity_str = f"{abs(activity.quantity)}"
        if activity.chemical.chemical_state == 'Liquid':
            quantity_str += 'L'
        else:
            quantity_str += 'g'
            
        activity_list.append({
            'action': activity.get_action_display(),
            'chemical': activity.chemical.name,
            'quantity': quantity_str,
            'user': activity.user.get_full_name(),
            'timestamp': activity.timestamp
        })

    # Calculate usage trends
    usage_trends = []
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30 * i)
        month_start = month_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        monthly_usage = ChemicalActivity.objects.filter(
            timestamp__date__range=[month_start, month_end],
            action__in=['used', 'removed']
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        usage_trends.append({
            'month': month_date.strftime('%b'),
            'usage': float(f"{monthly_usage:.2f}")
        })

    return Response({
        'total_chemicals': total_chemicals,
        'expired_chemicals': expired_chemicals,
        'low_stock_alerts': low_stock_alerts,
        'monthly_usage': current_month_usage,
        'monthly_usage_change': monthly_usage_change,
        'recent_activity': activity_list,
        'usage_trends': usage_trends
    })


@extend_schema(
    tags=['Reports'],
    description='Generate report (Legacy API)',
    parameters=[
        OpenApiParameter('report_type', OpenApiTypes.STR, enum=['inventory', 'usage', 'expiry', 'low-stock'], 
                        description='Report type'),
        OpenApiParameter('format', OpenApiTypes.STR, enum=['pdf', 'excel'], 
                        description='Report format'),
        OpenApiParameter('start_date', OpenApiTypes.DATE, 
                        description='Start date for report range'),
        OpenApiParameter('end_date', OpenApiTypes.DATE, 
                        description='End date for report range'),
        OpenApiParameter('days', OpenApiTypes.INT, 
                        description='Number of days to look ahead (for expiry report)'),
        OpenApiParameter('threshold', OpenApiTypes.FLOAT, 
                        description='Quantity threshold (for low-stock report)'),
    ],
    responses={
        200: {'type': 'string', 'format': 'binary'},
        400: {'description': 'Invalid parameters'},
        302: {'description': 'Redirects to specific report endpoint'}
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request):
    """
    Legacy report generation endpoint that redirects to the appropriate specific report endpoint.
    """
    from django.http import HttpResponseRedirect
    
    report_type = request.query_params.get('report_type')
    if not report_type:
        return Response({"error": "Missing report_type parameter"}, status=400)
    
    # Build the redirect URL
    params = request.query_params.copy()
    params.pop('report_type', None)  # Remove report_type from params
    
    # Convert report_type to the corresponding endpoint
    if report_type == 'inventory':
        endpoint = '/api/reports/inventory/'
    elif report_type == 'usage':
        endpoint = '/api/reports/usage/'
    elif report_type == 'expiry':
        endpoint = '/api/reports/expiry/'
    elif report_type == 'low-stock':
        endpoint = '/api/reports/low-stock/'
    else:
        return Response({"error": f"Invalid report type: {report_type}"}, status=400)
    
    # Build the query string
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    if query_string:
        redirect_url = f"{endpoint}?{query_string}"
    else:
        redirect_url = endpoint
    
    return HttpResponseRedirect(redirect_url)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_single_report(request, report_type):
    """
    Simple unified endpoint for generating all types of reports.
    Parameters:
    - report_type: inventory, usage, or expiry
    - format: 'pdf' or 'excel' (default: pdf)
    - start_date: Start date for report range (YYYY-MM-DD)
    - end_date: End date for report range (YYYY-MM-DD)
    """
    from django.http import HttpResponseRedirect
    
    # Get parameters
    params = request.query_params.copy()
    
    # Convert report_type to the corresponding endpoint
        if report_type == 'inventory':
        endpoint = '/api/reports/inventory/'
        elif report_type == 'usage':
        endpoint = '/api/reports/usage/'
        elif report_type == 'expiry':
        endpoint = '/api/reports/expiry/'
    elif report_type == 'low-stock':
        endpoint = '/api/reports/low-stock/'
        else:
        return Response({"error": f"Invalid report type: {report_type}. Must be one of: inventory, usage, expiry, low-stock"}, status=400)
    
    # Build the query string
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    if query_string:
        redirect_url = f"{endpoint}?{query_string}"
    else:
        redirect_url = endpoint
    
    return HttpResponseRedirect(redirect_url)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def simple_report(request, report_type):
    """
    Simple unified endpoint for generating all types of reports.
    """
    from django.http import HttpResponseRedirect
    
    # Get parameters
    params = request.query_params.copy()
    
    # Convert report_type to the corresponding endpoint
        if report_type == 'inventory':
        endpoint = '/api/reports/inventory/'
        elif report_type == 'usage':
        endpoint = '/api/reports/usage/'
        elif report_type == 'expiry':
        endpoint = '/api/reports/expiry/'
    elif report_type == 'low-stock':
        endpoint = '/api/reports/low-stock/'
    else:
        return Response({"error": f"Invalid report type: {report_type}. Must be one of: inventory, usage, expiry, low-stock"}, status=400)
    
    # Build the query string
    query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
    if query_string:
        redirect_url = f"{endpoint}?{query_string}"
        else:
        redirect_url = endpoint
    
    return HttpResponseRedirect(redirect_url)