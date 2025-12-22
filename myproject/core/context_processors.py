# context_processors.py
from .models import SiteSetting, Category

def site_info(request):

    settings = SiteSetting.objects.first()

    categories = Category.objects.filter(is_active=True).order_by('order')

    if settings:
        return {
            'site_settings': settings, 
            'global_categories': categories[:4], 
            'all_categories': categories, 
        }
    return {
        'site_settings': None,
        'global_categories': [],
    }