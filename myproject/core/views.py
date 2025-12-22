from django.shortcuts import render, get_object_or_404
from .models import  Product, StaticPage, AboutPageContent, WhyChooseReason, ContactPageSettings


def home_view(request):
    # Get Best Seller Products (limited to 8)
    best_sellers = Product.objects.filter(is_best_seller=True).order_by('order')[:8]

    context = {
        'products': best_sellers, 
    }

    return render(request, 'homepage.html', context)


def products_view(request):
    # Get category slug from query parameters
    active_category_slug = request.GET.get('category')

    # Filter products
    if active_category_slug and active_category_slug != '':
        products_list = Product.objects.filter(
            category__slug=active_category_slug 
        ).order_by('name')
    else:
        products_list = Product.objects.all().order_by('name')

    context = {
        'products': products_list,
        'active_category': active_category_slug,  
    }

    return render(request, 'products.html', context)

def about_view(request):
    # About Page Content
    about_content = get_object_or_404(AboutPageContent, pk=1)

    # Why Choose Us reasons
    why_reasons = WhyChooseReason.objects.all().order_by('order')

    context = {
        # About Header
        'about_main_title': about_content.about_main_title,
        'about_subtitle': about_content.about_subtitle,

        # About Story Section
        'about_main_image': about_content.about_main_image.url if about_content.about_main_image else None,
        'about_story_title': about_content.about_story_title,
        'about_story_p1': about_content.about_story_p1,
        'about_story_p2': about_content.about_story_p2,

        # Why Choose Us
        'why_choose_title': about_content.why_choose_title,
        'why_choose_subtitle': about_content.why_choose_subtitle,
        'why_reasons': why_reasons,

        # Call To Action
        'taste_title': about_content.taste_title,
        'taste_desc': about_content.taste_desc,
        'taste_image': about_content.taste_image.url if about_content.taste_image else None,
    }

    return render(request, 'aboutus.html', context)

def contact_view(request):
    # Contact Page Settings
    contact_settings = get_object_or_404(ContactPageSettings, pk=1)

    # Best Selling Products
    best_sellers = Product.objects.filter(
        is_best_seller=True
    ).order_by('order')[:4]

    context = {
        # Header Section
        'contact_us_title': contact_settings.contact_us_title,
        'contact_page_subtext': contact_settings.contact_page_subtext,

        # Contact Info Section
        'contact_heading': contact_settings.contact_heading,
        'contact_description': contact_settings.contact_description,
        'contact_image': contact_settings.contact_image.url if contact_settings.contact_image else None,

        # Best Sellers
        'best_sellers_title': contact_settings.best_sellers_title,
        'best_sellers_subtitle': contact_settings.best_sellers_subtitle,
        'products': best_sellers,

        # Call To Action
        'taste_title': contact_settings.taste_title,
        'taste_desc': contact_settings.taste_desc,
        'taste_image': contact_settings.taste_image.url if contact_settings.taste_image else None,
    }

    return render(request, 'contact.html', context)


def static_page_view(request, slug):
    page = get_object_or_404(StaticPage, slug=slug)

    context = {
        'page_title': page.title,
        'page_content': page.content,
    }
    return render(request, 'static_page.html', context)

def refund_policy_view(request):
    return static_page_view(request, slug='refund-policy')


def terms_conditions_view(request):
    return static_page_view(request, slug='terms-conditions')


def privacy_policy_view(request):
    return static_page_view(request, slug='privacy-policy')