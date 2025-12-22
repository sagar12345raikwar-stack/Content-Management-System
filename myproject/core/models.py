from unicodedata import category
from django.db import models
from django.utils.text import slugify

class SiteSetting(models.Model):

    navbar_logo = models.ImageField(
        upload_to='site_logos/',
        null=True, 
        blank=True, 
        help_text="Upload the image for the main Navbar logo."
    )
    footer_logo = models.ImageField(
        upload_to='site_logos/',
        null=True, 
        blank=True, 
        help_text="Upload the image for the Footer logo."
    )
    hero_image = models.ImageField(
        upload_to='site_images/',
        null=True, 
        blank=True, 
        help_text="Upload the hero image for the homepage."
    )
    tradition_image = models.ImageField(
        upload_to='site_images/',
        null=True, 
        blank=True, 
        help_text="Upload the tradition image for the homepage"
    )
    still_craving_image = models.ImageField(
        upload_to='site_images/',
        null=True, 
        blank=True, 
        help_text="Upload the still creaving section image for the homepage"
    )
    
    site_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, default="918965756562", help_text="WhatsApp number without '+'. Used in links.")
    contact_email = models.EmailField()
    location = models.CharField(max_length=255)
    copyright_holder = models.CharField(max_length=100)

    # Hero Section Content
    hero_title = models.TextField()
    hero_subtext = models.TextField()
    
    # Tradition Section Content
    tradition_title = models.CharField(max_length=255)
    tradition_paragraph1 = models.TextField()
    tradition_paragraph2 = models.TextField()

    # Best Sellers Section Content
    best_sellers_title = models.CharField(max_length=255)
    best_sellers_subtitle = models.CharField(max_length=255)
    
    # Still Craving Section Content
    still_craving_title = models.CharField(max_length=255)
    still_craving_subtext = models.CharField(max_length=255)

    # Footer Content
    footer_description = models.TextField()

    # Products Section Content (Add these)
    products_title = models.CharField(
        max_length=255, 
        default="Explore Our Products", 
        help_text="Title for the products section on the homepage."
    )
    products_subtitle = models.TextField(
        default="Discover everything we make with care, love, and authentic Andhra taste.",
        help_text="Subtitle for the products section."
    )

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Enforce that only one instance of SiteSetting exists
        if SiteSetting.objects.exists() and not self.pk:
            raise Exception("There can be only one SiteSetting instance.")
        return super(SiteSetting, self).save(*args, **kwargs)



class Category(models.Model):
    category_image =models.ImageField(
    upload_to='category_images/',
    blank=True,
    null=True,
    help_text="Category image for the Categories Section.") 

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, help_text="URL-friendly version of the title.")
    is_active = models.BooleanField(default=True, help_text="Show this category on the home page and products page.")
    order = models.IntegerField(default=0, help_text="Order in which categories appear.")

    class Meta:
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)



class Product(models.Model):
    """
    Model for individual products, especially for the 'Best Sellers' section.
    """
    product_image =models.ImageField(
        upload_to='products_images/',
        null=True,
        blank=True, 
        help_text="Product image for the product.")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in Indian Rupees (₹)")
    unit = models.CharField(max_length=50, default="kg", help_text="e.g., 'kg', 'piece', 'box'")
    
    is_best_seller = models.BooleanField(default=False, help_text="Check to display in the 'Best Sellers' section on the homepage.")
    order = models.IntegerField(default=0, help_text="Order within the 'Best Sellers' section.")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.category.title})"
    
    @property
    def whatsapp_text(self):
        """Generates a default WhatsApp order message for the product."""
        # URL-safe text for 'I want to order [product name]'
        return f"I want to order {self.name}".replace(" ", "%20")

class StaticPage(models.Model):

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, help_text="Used in the URL, e.g., 'refund-policy'")
    content = models.TextField(help_text="Full HTML content for the policy page.")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Static Policy Page"
        verbose_name_plural = "Static Policy Pages"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class AboutPageContent(models.Model):

    # Header Section
    about_main_title = models.CharField(max_length=255, default="About Nellore Maharuchulu")
    about_subtitle = models.CharField(max_length=255, default="Bringing the flavors of Andhra’s kitchens to your home.")
    
    # Image + Text Section (Our Story)
    about_main_image = models.ImageField(upload_to='about/', help_text="Large image for the main story section.")
    about_story_title = models.CharField(max_length=255, default="Homemade Flavours, Straight from Nellore")
    about_story_p1 = models.TextField(default="What started in our family kitchen is now reaching kitchens across the country. Nellore Maharuchulu was born from a simple idea...")
    about_story_p2 = models.TextField(default="From sun-dried spice powders to oil-cured pickles and hand-rolled laddus, every item is prepared using locally sourced ingredients and age-old recipes...")

    # Why Choose Us Section
    why_choose_title = models.CharField(max_length=255, default="Why Choose Us")
    why_choose_subtitle = models.TextField(default="At Nellore Maharuchulu, we don’t just make food — we preserve tradition...")

    # Call To Action (Taste Tradition Section)
    taste_title = models.CharField(max_length=255, default="Ready to Taste the Tradition?")
    taste_desc = models.CharField(max_length=255, default="Browse our handmade spice powders, pickles, laddus, and more — and order easily through WhatsApp.")
    taste_image = models.ImageField(upload_to='about/cta/', help_text="Small spice stack image for the CTA section.")
    
    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"
        
    def __str__(self):
        return self.about_main_title
        
    def save(self, *args, **kwargs):
        # Enforce that only one instance exists
        if AboutPageContent.objects.exists() and not self.pk:
            raise Exception("There can be only one AboutPageContent instance.")
        return super(AboutPageContent, self).save(*args, **kwargs)

class WhyChooseReason(models.Model):

    """
    Model for the repeating cards in the 'Why Choose Us' section.
    """
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=300)
    icon = models.ImageField(upload_to='about/icons/', help_text="Small icon image for the card (e.g., 48x48)")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Why Choose Reason"
        verbose_name_plural = "Why Choose Reasons"
        ordering = ['order']

    def __str__(self):
        return self.title

class ContactPageSettings(models.Model):
    """
    Singleton model to hold dynamic text and images specific to the Contact Us page.
    """
    # Header Section
    contact_us_title = models.CharField(
        max_length=100, 
        default="Contact Us",
        help_text="The main title at the top of the contact page."
    )
    contact_page_subtext = models.TextField(
        default="We’d love to hear from you — whether it’s for orders, feedback, or questions about our products.",
        help_text="The descriptive subtext under the main Contact Us title."
    )

    # Contact Info Section
    contact_heading = models.CharField(
        max_length=200, 
        default="We’re Just a Message Away",
        help_text="The main heading for the contact details section."
    )
    contact_description = models.TextField(
        default="Our team is dedicated to bringing you the best flavors and service. Reach out to us via phone, email, or visit our location during business hours.",
        help_text="The descriptive paragraph under the main contact heading."
    )
    contact_image = models.ImageField(
        upload_to='page_images/', 
        help_text="Image displayed next to the contact details (e.g., a hand-made item photo)."
    )
    
    # Best Sellers Section (for this page)
    best_sellers_title = models.CharField(
        max_length=150, 
        default="Tried and Tested",
        help_text="Title for the best sellers section on the contact page."
    )
    best_sellers_subtitle = models.CharField(
        max_length=255, 
        default="See what everyone's ordering right now—the best of Nellore Maharuchulu.",
        help_text="Subtitle for the best sellers section on the contact page."
    )
    
    # Call To Action (CTA) Section - Reusing fields from the template
    taste_title = models.CharField(
        max_length=150, 
        default="Ready to Taste the Tradition?",
        help_text="Title for the final call-to-action bar."
    )
    taste_desc = models.CharField(
        max_length=255, 
        default="Browse our handmade spice powders, pickles, sweets, and instant mixes.",
        help_text="Description for the final call-to-action bar."
    )
    taste_image = models.ImageField(
        upload_to='page_images/', 
        default='images/top-view-condiments-frame-with-copy-space-Photoroom.png',
        help_text="Image displayed next to the final CTA text."
    )
    
    class Meta:
        verbose_name = "Contact Page Setting"
        verbose_name_plural = "Contact Page Settings"

    def __str__(self):
        return "Contact Page Content Settings"

    def save(self, *args, **kwargs):
        # Enforce that only one instance exists
        if ContactPageSettings.objects.exists() and not self.pk:
            raise Exception("There can be only one ContactPageSettings instance.")
        return super(ContactPageSettings, self).save(*args, **kwargs)