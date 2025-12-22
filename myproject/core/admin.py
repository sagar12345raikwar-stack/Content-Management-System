from django.contrib import admin
from .models import SiteSetting, Category, Product, StaticPage,AboutPageContent, WhyChooseReason,ContactPageSettings
from tinymce.widgets import TinyMCE
from django import forms


# Custom Admin for SiteSetting to ensure only one instance
class SiteSettingAdmin(admin.ModelAdmin):
    # Fieldsets for better organization in the admin
    fieldsets = (

        ('Logos & Branding', {
            'fields': ('navbar_logo', 'footer_logo'),
            'description': 'Configure the main site name and image assets.'
        }),
        ('Site Identity', {
            'fields': ('site_name', 'copyright_holder', 'footer_description'),
        }),
        ('Contact Information', {
            'fields': ('phone', 'whatsapp_number', 'contact_email', 'location'),
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtext','hero_image'),
        }),
        ('Tradition Section', {
            'fields': ('tradition_image','tradition_title', 'tradition_paragraph1', 'tradition_paragraph2'),
        }),
        ('Best Sellers Section', {
            'fields': ('best_sellers_title', 'best_sellers_subtitle'),
        }),
        ('Still Craving Section', {
            'fields': ('still_craving_image','still_craving_title', 'still_craving_subtext'),
        }),
        ('Product Page Content', {
            'fields': ('products_title','products_subtitle'),
        }),
    )
    # Disable 'Add' and 'Delete' to keep only one instance
    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(SiteSetting, SiteSettingAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price','product_image', 'unit', 'is_best_seller', 'order')
    list_filter = ('category', 'is_best_seller')
    list_editable = ('is_best_seller', 'order', 'price', 'unit')
    search_fields = ('name',)

class StaticPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = StaticPage
        fields = '__all__'

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    form = StaticPageAdminForm 
    list_display = ('title', 'slug', 'last_updated')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

class AboutPageContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Header Section', {
            'fields': ('about_main_title', 'about_subtitle'),
        }),
        ('Our Story Section (Image + Text)', {
            'fields': ('about_story_title', 'about_main_image', 'about_story_p1', 'about_story_p2'),
        }),
        ('Why Choose Us Section', {
            'fields': ('why_choose_title', 'why_choose_subtitle'),
        }),
        ('Call To Action Section', {
            'fields': ('taste_title', 'taste_desc', 'taste_image'),
        }),
    )

    def has_add_permission(self, request):
        return not AboutPageContent.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(AboutPageContent, AboutPageContentAdmin)

@admin.register(WhyChooseReason)
class WhyChooseReasonAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'icon')
    list_editable = ('order',)
    search_fields = ('title',)

@admin.register(ContactPageSettings)
class ContactPageSettingsAdmin(admin.ModelAdmin):
    # Organizes the fields in the admin form
    fieldsets = (
        ('Header Section', {
            'fields': ('contact_us_title', 'contact_page_subtext'),
            'description': 'Text that appears right at the top of the page.',
        }),
        ('Contact Info Section', {
            'fields': ('contact_heading', 'contact_description', 'contact_image'),
            'description': 'Details and image next to the contact information.',
        }),
        ('Best Sellers Section Text', {
            'fields': ('best_sellers_title', 'best_sellers_subtitle'),
        }),
        ('Call To Action (CTA) Section', {
            'fields': ('taste_title', 'taste_desc', 'taste_image'),
            'description': 'Settings for the final call-to-action bar at the bottom.',
        }),
    )

    # Enforce Singleton pattern: Disable 'Add' button and 'Delete' button
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
    list_display = ('__str__',)

    # Redirects back to the edit page after saving
    def response_change(self, request, obj):
        if "_save" in request.POST:
            return self.response_post_save_change(request, obj)
        return super().response_change(request, obj)