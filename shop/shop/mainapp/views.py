from django.shortcuts import render

from django.http import HttpResponseRedirect

from django.views.generic import DetailView, View

from django.contrib.contenttypes.models import ContentType

from .models import Notebooks, Smartphones, Category, LatestProducts, Customer, Cart,CartProduct

from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart=Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories()
        products = LatestProducts.objects.get_products_for_main_page('notebooks', 'smartphones')
        context = {'categories': categories,
                   'products': products,
                   'cart': cart}
        return render(request, 'base.html', context)


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebooks': Notebooks,
        'smartphones': Smartphones,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class AddToCartView(View):


    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer, in_order=False)
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.create(
            user=cart.owner, cart=cart, content_object=product, final_price=product.price

        )
        print(dir(CartProduct))
        cart.products.add(cart_product)
        cart.save()

        return HttpResponseRedirect('/cart/')


class CartView(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories()
        context = {
            'cart': cart,
            'categories': categories,
        }
        return render(request, 'cart.html', context)
