from django.db import models

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    thumbnail = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductVariant(models.Model):
    id = models.BigAutoField(primary_key=True)
    variant = models.CharField(max_length=255)
    variant_id = models.ForeignKey('self', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductVariantPrice(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_variant_one = models.ForeignKey(ProductVariant, related_name='variant_one', on_delete=models.CASCADE)
    product_variant_two = models.ForeignKey(ProductVariant, related_name='variant_two', on_delete=models.CASCADE)
    product_variant_three = models.ForeignKey(ProductVariant, related_name='variant_three', on_delete=models.CASCADE)
    price = models.FloatField()
    stock = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Variant(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
