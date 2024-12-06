from django.db import models

# Create your models here.
class UserLogin(models.Model):
    username=models.CharField(max_length=50,null=True)
    password=models.CharField(max_length=50,null=True)
    utype=models.CharField(max_length=50,null=True)

class UserReg(models.Model):
    usertype=models.CharField(max_length=50,null=True)
    username=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50,null=True)
    number=models.CharField(max_length=50,null=True)
    password=models.CharField(max_length=50,null=True)

class AddItem(models.Model):
    Item_code=models.CharField(max_length=50,null=True)
    Item_name=models.CharField(max_length=50,null=True)
    Item_GST=models.CharField(max_length=50,null=True)
    Item_price=models.CharField(max_length=50,null=True)
    Category=models.CharField(max_length=50,null=True)


class AddTable(models.Model):
    Table_name=models.CharField(max_length=50,null=True)
    Category=models.CharField(max_length=50,null=True)

class AddCompany(models.Model):
    Company_name=models.CharField(max_length=50,null=True)
    Company_address=models.CharField(max_length=50,null=True)
    Company_GST=models.CharField(max_length=50,null=True)
    Company_number=models.CharField(max_length=50,null=True)

class ItemOrder(models.Model):
    table_name = models.CharField(max_length=100,null=True)
    bill_no = models.CharField(max_length=100,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=100,null=True)
    item_name = models.CharField(max_length=100,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    item_cat= models.CharField(max_length=100,null=True)

class Orders(models.Model):
    table_name = models.CharField(max_length=100,null=True)
    bill_no = models.CharField(max_length=100,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=100,null=True)
    item_name = models.CharField(max_length=100,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    item_cat = models.CharField(max_length=100, null=True)

class Printorders(models.Model):
    table_name = models.CharField(max_length=100,null=True)
    bill_no = models.CharField(max_length=100,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=100,null=True)
    item_name = models.CharField(max_length=100,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    item_cat = models.CharField(max_length=100, null=True)


class Pracel(models.Model):
    bill_no = models.CharField(max_length=100,null=True)
    bill_date = models.DateField()
    bill_time = models.TimeField(null=True)
    item_code = models.CharField(max_length=100,null=True)
    item_name = models.CharField(max_length=100,null=True)  # Add this field if not already present
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    gst = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    qty = models.IntegerField()
    tax_amt = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total_gst = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    pracel_charge = models.DecimalField(max_digits=10, decimal_places=2,null=True)

class Expenses(models.Model):
    Date=models.DateField(null=True)
    Reason=models.CharField(max_length=150,null=True)
    Amount=models.CharField(max_length=150,null=True)
    staffname = models.CharField(max_length=150, null=True)

class Salary(models.Model):
    Date=models.DateField(null=True)
    desc=models.CharField(max_length=150,null=True)
    Amount=models.CharField(max_length=150,null=True)
    staffname = models.CharField(max_length=150, null=True)