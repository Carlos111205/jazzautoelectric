from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, default='fas fa-cogs', help_text="FontAwesome class name, e.g., 'fas fa-car-battery'")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='parts')
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="SKU/Part Number")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    image = models.ImageField(upload_to='parts/', blank=True, null=True, help_text="Upload part image")
    is_available = models.BooleanField(default=True, verbose_name="In Stock")
    specifications = models.TextField(blank=True, help_text="Format: Key: Value, one per line")

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sku if self.sku else 'No SKU'})"

    def get_specifications_list(self):
        if not self.specifications:
            return []
        specs = []
        for line in self.specifications.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                specs.append({'key': key.strip(), 'value': val.strip()})
            elif line.strip():
                specs.append({'key': 'Spec', 'value': line.strip()})
        return specs
