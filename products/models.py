from email.mime import image
from django.db import models
from django.utils.translation import gettext as _
from authentication.models import User



CATEGORY_CHOICES = [
    ("men-clothing", "Men Clothing"),
    ("women-clothing", "Women Clothing"),
    ("kids-clothing", "Kids Clothing"),
    ("watches", "Watches"),
    ("shoes & handbag", "Shoes & Handball"),
    ("books", "Books"),
    ("home & kitchen", "Home & Kitchen"),
    ("health & personalcares", "Health & Personalcares"),
    ("gifts", "gifts"),
]

class Product(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"),  on_delete=models.CASCADE )
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(_('stock'), default=1)
    category = models.CharField(_('Category'), choices=CATEGORY_CHOICES, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    image = models.ImageField(upload_to='product-image/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)