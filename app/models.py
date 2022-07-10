from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

COUNTY_CHOICES = (
    
    ('Carlow' , 'Carlow'),
    ('Cavan', 'Cavan'),
    ('Clare','Clare'),
    ('Cork','Cork'),
    ('Donegal','Donegal'),
    ('Dublin','Dublin'),
    ('Galway','Galway'),
    ('Kerry','Kerry'),
    ('Kildare','Kildare'),
    ('Kilkenny','Kilkenny'),
    ('Laois','Laois'),
    ('Leitrim','Leitrim'),
    ('Limerick','Limerick'),
    ('Longford','Longford'),
    ('Louth','Louth'),
    ('Mayo','Mayo'),
    ('Meath','Meath'),
    ('Monaghan','Monaghan'),
    ('Offaly','Offaly'),
    ('Roscommon','Roscommon'),
    ('Sligo','Sligo'),
    ('Tipperary','Tipperary'),
    ('Waterford','Waterford'),
    ('Westmeath','Westmeath'),
    ('Wexford','Wexford'),
    ('Wicklow','Wicklow'),
    
)

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    eircode = models.CharField(max_length=50, unique=True, validators=[alphanumeric])
    county = models.CharField(choices = COUNTY_CHOICES, max_length=50)
  
    
def __str__(self):
    return str(self.id)



CATEGORY_CHOICES = (
    ('V','Vegetables'),
    ('F', 'Fruits'),
    ('G','Grocery'),
    ('D','Dairy'),
    
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    supplier = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to = 'productimg')
 
    
def __str__(self):
    return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

def __str__(self):
    return str(self.id)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way', 'On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')
    