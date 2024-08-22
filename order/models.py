from ast import Return
from itertools import product
from typing import Iterable
from django.db import models
from authentication.models import User
from products.models import Product
from django.utils.translation import gettext as _

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"), null=True, blank=True)
    total_price = models.DecimalField(_("Total Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        return super(Order, self).save()
    
    def __str__(self):
        return f"{self.product.name} by {self.user.username}"