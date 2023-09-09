from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from djmoney.models.fields import MoneyField
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

PART_CHOICES = [
    ('CPU', 'CPU'),
    ('Motherboard', 'Motherboard'),
    ('Graphics card', 'Graphics card'),
    ('Case', 'Case'),
    ('Power Supply', 'Power Supply'),
    ('Memory', 'Memory'),
    ('Storage', 'Storage'),
    ('Sound card', 'Sound card'),
    ('Additional fans', 'Additional fans'),
    ('Wireless networking', 'Wireless networking'),
    ('Bluetooth card', 'Bluetooth card'),
    ('Monitor', 'Monitor'),
    ('Keyboard', 'Keyboard'),
    ('Mouse', 'Mouse'),
    ('Mouse pad', 'Mouse pad'),
    ('Microphone', 'Microphone'),
    ('Headset', 'Headset'),
    ('Operating system', 'Operating system'),
    ('CPU cooler', 'CPU cooler'),
    ('Mouse', 'Mouse'),
]


class UserPayment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now=True)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        if instance.is_authenticated:
            new_user_payment = UserPayment.objects.create(user=instance)
            new_user_payment.save()



class Part(models.Model):
    
    part_name = models.CharField(max_length=75)
    type = models.CharField(choices=PART_CHOICES, max_length=30, default="")
    price_in_pence = models.IntegerField(default=0)
    link = models.CharField(max_length=500)

    def getprice(self):

        price = self.price_in_pence
        price = price / 100
        return ('%.2f' %price)


class Product(models.Model):

    slug = models.SlugField(max_length=100, unique=True, blank=True)
    product_name = models.CharField(max_length=75)
    price_in_pence = models.IntegerField(default=0)
    image = models.ImageField(upload_to = 'images/')
    sold = models.BooleanField(default=True)
    parts = models.ManyToManyField(Part)


    def getprice(self):

        price = self.price_in_pence
        price = price / 100
        return ('%.2f' %price)

    
    '''case = models.ForeignKey(Part, on_delete=models.SET_NULL)
    cpu = models.ForeignKey(Part, on_delete=models.SET_NULL)
    power_supply = models.ForeignKey(Part, on_delete=models.SET_NULL)
    motherboard = models.ForeignKey(Part, on_delete=models.SET_NULL)
    memory = models.ForeignKey(Part, on_delete=models.SET_NULL)
    gpu = models.ForeignKey(Part, on_delete=models.SET_NULL)
    primary_hard_drive = models.ForeignKey(Part, on_delete=models.SET_NULL)
    secondary_hard_drive = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    
    sound_card = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    additional_fans = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    wireless_networking = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    bluetooth = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    monitor = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    keyboard = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    mouse = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    mouse_pad = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    microphone = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    headset = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    operating_system = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    cpu_cooler = models.ForeignKey(Part, default=None, blank=True, null=True, on_delete=models.SET_NULL)'''

    def __str__(self):
        return self.product_name
    
    
    def get_absolute_url(self):
        return ('productPage', { 'slug' : self.slug })


def create_slug(instance, new_slug = None):

    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    try:
        qs = Product.objects.filter(slug=slug).order_by("-id")
        exists = qs.exists
        if exists:
            new_slug = "%s-%s"%(slug,qs.first().id)
            return create_slug(instance, new_slug=new_slug)
    except:
        pass
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)
    
'''
class Review(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(
    validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],)
    review = models.CharField(max_length=500)
    image1 = models.ImageField(blank=True, upload_to = 'images/')
    image2 = models.ImageField(blank=True, upload_to = 'images/')
'''



