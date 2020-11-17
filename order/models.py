from django.db import models
from django.core.validators import RegexValidator

class Coffee(models.Model):
    name = models.CharField(max_length= 1000 , blank=True)
    amount = models.CharField(max_length=100 , blank=True)
    order_id = models.CharField(max_length=1000 )
    razorpay_payment_id = models.CharField(max_length=1000 ,blank=True)
    currency = models.CharField(max_length=100,blank=True,null=True)
    email_id = models.EmailField(verbose_name="Email",max_length=64,unique=True,blank=True,null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    mobile_number = models.CharField(verbose_name="Mobile Number",validators=[phone_regex],max_length=15,unique=True,blank=True,null=True)
    paid = models.BooleanField(default=False)