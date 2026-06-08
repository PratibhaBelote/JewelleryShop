from django.db import models

# Common choices
CATEGORY_CHOICES = [
    ('Gold', 'Gold'),
    ('Silver', 'Silver'),
    ('Platinum', 'Platinum'),
]

PAYMENT_STATUS_CHOICES = [
    ('Paid', 'Paid'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
]

# Jewellery Item model
class JewelleryItem(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    purity = models.CharField(max_length=50)
    weight = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.category})"

# Sale model
class Sale(models.Model):
    sale_date = models.DateField()  # Allow user to select date manually
    customer_name = models.CharField(max_length=100, default='Unknown Customer')
    product_name = models.CharField(max_length=100, default='Unknown Product')
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.customer_name} - {self.product_name} ({self.sale_date})"

# Customer model
class Customer(models.Model):
    name = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, default='N/A')
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])

    def __str__(self):
        return self.name
