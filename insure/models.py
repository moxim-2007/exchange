from django.db import models
import uuid

from account.models import Company


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return "{}".format(self.name)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return "Product {}".format(self.name)


class ProductInfo(models.Model):
    price = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "Information of {}".format(self.product.name)


class Response(models.Model):
    full_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "Response to {}".format(self.product.name)
