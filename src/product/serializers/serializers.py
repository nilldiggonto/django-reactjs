from product.models import *
from rest_framework import serializers

# class ProductVariantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductVariant
#         fields = ['variant_title',]

class ProductVariantPriceSerializer(serializers.ModelSerializer):
    variant_one_title = serializers.CharField(source='product_variant_one.variant_title', allow_blank=True, allow_null=True)
    variant_two_title = serializers.CharField(source='product_variant_two.variant_title', allow_blank=True, allow_null=True)
    variant_three_title = serializers.CharField(source='product_variant_three.variant_title', allow_blank=True, allow_null=True)
    class Meta:
        model = ProductVariantPrice
        fields = ['id', 'variant_one_title','variant_two_title','variant_three_title', 'price', 'stock']

class ProductListSerializer(serializers.ModelSerializer):
    # product_variants = serializers.SerializerMethodField()
    product_variants_sales = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'sku', 'description','product_variants_sales']
    
    # def get_product_variants(self, obj):
    #     variants = ProductVariant.objects.filter(product_id=obj.id)
    #     # serializer = ProductVariantSerializer(variants, many=True)
    #     return serializer.data
    
    def get_product_variants_sales(self, obj):
        variants_price = ProductVariantPrice.objects.filter(product_id=obj.id)
        serializer = ProductVariantPriceSerializer(variants_price, many=True)
        return serializer.data