from django.db import models
class SignUpData(models.Model):
    sign_name=models.CharField(max_length=100,blank=False)
    sign_email=models.EmailField(max_length=100,blank=False,unique=True)
    sign_password=models.CharField(max_length=100, blank=False)
    sign_time= models.DateTimeField(blank=False, auto_now=True)
    secure_key = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.sign_name
    class Meta:
        db_table="users_data"



class Product(models.Model):
    id=models.AutoField(primary_key=True)
    category_choices = (("Home", "Home"), ("Jewelry", "Jewelry"), ("Electronics", "Electronics"), ("Clothes","Clothers"),("Others","Others"))
    category = models.CharField(max_length=100, blank=False,choices=category_choices)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=200,blank=False)
    price = models.PositiveIntegerField(blank=False)
    image = models.FileField(blank=False,upload_to="productimages")
    secure_key = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product_table"

class cart(models.Model):
    mail=models.CharField(max_length=30,blank=False)
    pid=models.IntegerField(max_length=10,blank=False)
    def __str__(self):
        return self.mail
    class Meta:
        db_table="cart_table"

class UploadedFile(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
