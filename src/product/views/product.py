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
            print(type(float(starting_price)))
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
        # query = request.GET.get('q')
        # title = request.GET.get('title',None)
        # variant = request.GET.get('variant',None)
        # starting_price = request.GET.get('starting_price',None)
        # ending_price = request.GET.get('ending_price',None)
        # time = request.GET.get('time',None)

        # #if time convert time to qs for django
        # products = None
        # if time and title is None and variant is None and starting_price is None and ending_price is None:
        #     time = datetime.datetime.strptime(time, '%Y-%m-%d')
        #     products = Product.objects.filter(created_at__year=time.year, created_at__month=time.month, created_at__day=time.day)
        
        # if title  and time is None and variant is None and starting_price is None and ending_price is None:
        #     products = Product.objects.filter(title__icontains=title)
        
        # if variant and time is None and title is None and starting_price is None and ending_price is None:
        #     variants = ProductVariant.objects.filter(variant_title=variant)
        #     products = [v.product for v in variants]
        
        # if starting_price and ending_price and time is None and title is None and variant is None:
        #     variants = ProductVariantPrice.objects.filter(price__gte=starting_price, price__lte=ending_price)
        #     products = [v.product for v in variants]

        # if title and variant and time and starting_price and ending_price:
        #     time = datetime.datetime.strptime(time, '%Y-%m-%d')

        #     variants = ProductVariantPrice.objects.filter(price__gte=starting_price, price__lte=ending_price)
        #     products = [v.product for v in variants]
        #     products = Product.objects.filter(title__icontains=title, pk__in=[p.pk for p in products])
        #     products = products.filter(created_at__year=time.year, created_at__month=time.month, created_at__day=time.day)

        #     variant = ProductVariant.objects.filter(variant_title=variant)
        #     v_products = [v.product for v in variant]
        #     products = products.filter(pk__in=[p.pk for p in v_products])

        # serializer = ProductListSerializer(products, many=True)
        # return Response(serializer.data)