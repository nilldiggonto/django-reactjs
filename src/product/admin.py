from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(ProductVariantPrice)


