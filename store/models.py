from django.db import models

# We don't need to add ID field as django creates that for each model automatically
# If we don't want django to create ID itself we need to make attribute primary_key=True in the required attribute

# Relations: 1tom
""" 

collection - product
customer - order
order - item
cart - item
It is defined by defining a foreign key in one of the related classes
We define relation in one class and django automatically makes the reverse relation
"""

# Many to many relation between promotion and product
class Promotion(models.Model):
    description = models.TextField()
    discount = models.FloatField()
    # Django will create here product_set as the reverse relation

# Collection is categories of products
# Circular dependency: When we have more than 1 relations between two classes then it creates circular dependency i.e. both classes depend on each other
class Collection(models.Model):
    title = models.CharField(max_length=255)
    # Circular dependency is handled by defining the related class type as '@classname'
    # Here we set related_name = '+' so that django will not create reverse relation 
    featured_product = models.ForeignKey(
        'Product', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='+'
        ) 

class Product(models.Model):
    title = models.CharField(max_length=255)
    # Slug is a non-nullable field so we need to define a default value or make it nullable
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True) # auto_now updates datetime whenever object is updated
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion)


class Customer(models.Model):
    BRONZE_MEMBER = "B"
    SILVER_MEMBER = "S"
    GOLD_MEMBER = "G"

    MEMBERSHIP_CHOICES = [
        (BRONZE_MEMBER, "Bronze"),
        (SILVER_MEMBER, "Silver"),
        (GOLD_MEMBER, "Gold")
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=BRONZE_MEMBER)

    # Metadata
    class Meta:
        # Table name we want to give
        db_table = 'store_customers'
        # To define SQL indexes
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]


class Order(models.Model):
    PENDING = "P"
    COMPLETE = "C"
    FAILED = "F"
    
    PAYMENT_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
        (FAILED, "Failed")
    ]

    # auto_now_add tells django to populate the table when the first time we create an instance of this class
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_statud = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

# Creating one-to-one relations
# We create an address class such that each customer can have 1 address and each address belongs to 1 customer
# Here we make customer as PK thus creating 1to1 relation
"""
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer,  on_delete=models.CASCADE, primary_key=True)
"""

# Creating one-to-many relations
# Here we make customer as FK thus creating 1tom relation
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,  on_delete=models.CASCADE)
    zip = models.CharField(max_length=255)