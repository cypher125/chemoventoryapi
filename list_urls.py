import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemoventry.settings')
django.setup()

# Import URL patterns
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

def list_urls(urlpatterns, prefix=''):
    """Recursively print out all URL patterns."""
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            print(f"{prefix}{pattern.pattern}")
        elif isinstance(pattern, URLResolver):
            print(f"{prefix}{pattern.pattern}")
            list_urls(pattern.url_patterns, prefix + str(pattern.pattern))

if __name__ == '__main__':
    resolver = get_resolver()
    list_urls(resolver.url_patterns)
    print("\nDone listing URLs.") 