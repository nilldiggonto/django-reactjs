from django.views import generic

from product.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from product.serializers.serializers import ProductListSerializer
import datetime
from django.db.models import Q

class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

# Showing Product List 
    
class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request,*args,**kwargs):
        name = request.data.get('name')
        sku = request.data.get('sku')
        description = request.data.get('description')
        image = request.data.get('image')
        variants = request.data.get('variants', [])
        prices = request.data.get('variant_prices', [])

        if not all([name, sku, description, image]):
            return Response({"error": "Missing required fields"})

        if variants and not isinstance(variants, list):
            return Response({"error": "Variants should be a list"})
        
        product = Product.objects.create(
            title = name,
            sku = sku,
            description = description,
        )
        ProductImage.objects.create(
            product = product,
        )

        variant_list = []

        for variant in variants:
            title = ""
            if variant.get('option') == 1:
                title = "Size"
            elif variant.get('option') == 2:
                title = "Color"
            else:
                title = "Style"

            v,_ =Variant.objects.get_or_create(
                title = title
            )
            for tag in variant.get('tags'):
                p_variant =ProductVariant.objects.create(
                    product = product,
                    variant_title = tag,
                    variant = v
                )
                variant_list.append(p_variant)
        price = prices[0]
        ProductVariantPrice.objects.create(
            product_variant_one = variant_list[0],
            product_variant_two = variant_list[1],
            product_variant_three = variant_list[2],
            price = price['price'],
            stock = price['stock'],
            product = product
        )
                

        return Response({
            "name": name,
            "sku": sku,
            "description": description,
            "image": image,
            "variants": variants
        })
        

class ProductSearchAPIView(APIView):
    def get(self, request):
        title = request.GET.get('title', None)
        variant = request.GET.get('variant', None)
        starting_price = request.GET.get('starting_price', None)
        ending_price = request.GET.get('ending_price', None)
        time = request.GET.get('time', None)

        products = Product.objects.all()
        if variant:
            variants = ProductVariant.objects.filter(variant_title=variant)
            # products = products.filter(variants__in=variants)
            products = [v.product for v in variants]
            products = Product.objects.filter(pk__in=[p.pk for p in products])

        if starting_price and ending_price:
            # print(type(float(starting_price)))
            variants = ProductVariantPrice.objects.filter(price__gte=float(starting_price))
            variants = variants.filter(price__lte=float(ending_price))
            products = [v.product for v in variants]
            products = Product.objects.filter(pk__in=[p.pk for p in products])
        if title:
            products = products.filter(title__icontains=title)
        if time:
            time = datetime.datetime.strptime(time, '%Y-%m-%d')
            products = products.filter(created_at__year=time.year, created_at__month=time.month, created_at__day=time.day)

        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    