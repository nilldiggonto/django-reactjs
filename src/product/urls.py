from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView, ProductListAPIView,ProductSearchAPIView,ProductDetailsAPIView
from product.views.variant import VariantView, VariantCreateView, VariantEditView,VariantListAPIView
from .models import Variant
app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),

    path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
        'product': True,'variants': Variant.objects.filter(active=True),
    }), name='list.product'),

    #API URLS
    path('api/list/', ProductListAPIView.as_view(), name='api.product.list'),
    path('api/variant/list/', VariantListAPIView.as_view(), name='api.variant.list'),
    path('api/search/', ProductSearchAPIView.as_view(), name='api.product.search'),
    path('update/<int:product_id>/', CreateProductView.as_view(), name='create.product'),
    path('api/details/<int:product_id>/', ProductDetailsAPIView.as_view(), name='api.product.details'),

]
