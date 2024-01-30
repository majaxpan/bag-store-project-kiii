from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=2083, null=True)

    # bag specific fields
    CHAIN_CHOICES = [
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('no chain', 'No chain')
    ]
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    COLOR_CHOICES = [
        ("black", "Black"),
        ("white", "White"),
        ("red", "Red"),
        ("blue", "Blue"),
        ("yellow", "Yellow"),
        ("purple", "Purple"),
        ("green", "Green"),
        ("orange", "Orange"),
        ("pink", "Pink"),
        ("brown", "Brown"),
        ("gray", "Gray"),
    ]
    chain_type = models.CharField(max_length=10, choices=CHAIN_CHOICES, default="no chain")
    size_type = models.CharField(max_length=10, choices=SIZE_CHOICES, default="S")
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="black")

    def __str__(self):
        return self.name

    #comment later:
    # @property
    # def imageURL(self):
    #     try:
    #         url = self.image.url
    #     except AttributeError:
    #         url = ''
    #     return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    street_name = models.CharField(max_length=100, null=True)
    street_number = models.IntegerField()
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.street_name} {self.street_number}, {self.city}, {self.country}'