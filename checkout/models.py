import uuid
from django.db import models
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from services.models import Service
from profiles.models import UserProfile
from decimal import Decimal


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField(max_length=20)
    town_or_city = models.CharField(max_length=40)
    address_line_1 = models.CharField(max_length=80)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80)
    country = CountryField(blank_label='Country *')
    postcode = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, default=0)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='orders')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10,
                                      decimal_places=2, default=0)
    stripe_pid = models.CharField(max_length=254, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update total each time a line item is added
        """
        self.order_total = self.order_lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.coupon:
            self.discount = self.coupon.amount
            self.grand_total = Decimal(self.order_total - self.discount)
        else:
            self.order_total = self.grand_total
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_lineitems')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    size = models.CharField(max_length=2)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.service.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.service.name} on order {self.order.order_number}'


class Coupon(models.Model):
    name = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.name} {self.start_date} - {self.end_date}'
