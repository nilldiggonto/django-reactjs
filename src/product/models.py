from django.db import models
from config.g_model import TimeStampMixin
from django.core.files.base import ContentFile
import base64


# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku = models.SlugField(max_length=255, unique=True)
    description = models.TextField()



class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.ImageField(null=True,blank=True)

    def save_image_from_base64(self, base64_data):
        if base64_data.startswith('data:image'):
            # Split the base64 data to get the actual data part
            format, imgstr = base64_data.split(';base64,')
            # Decode the base64 data
            data = base64.b64decode(imgstr)
            # Create a ContentFile object from the decoded data
            file_name = 'image.png'  # You can set your desired file name here
            file = ContentFile(data, name=file_name)
            # Assign the ContentFile to the ImageField
            self.file_path.save(file_name, file, save=True)


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_variants')


class ProductVariantPrice(TimeStampMixin):
    product_variant_one = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_one')
    product_variant_two = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_two')
    product_variant_three = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                              related_name='product_variant_three')
    price = models.FloatField()
    stock = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
