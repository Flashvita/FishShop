from django.shortcuts import render
from django import views
from .models import Product, Category, UnderCategory, Customer, OrderProduct, Order
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm, ProductAddToCartForm, OrderCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from .cart import Cart
from .tasks import new_order


class BaseView(views.View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'base.html', context)


class CategoriesView(ListView):
    model = Category
    template_name = 'catalog/categories.html'
    context_object_name = 'categories'


class CategoryView(views.View):
    def get(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        under_categories = UnderCategory.objects.filter(category=category)
        context = {
            'under_categories': under_categories,

        }
        return render(request, 'catalog/category_detail.html', context)


class UnderCategoryView(views.View):
    def get(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        under_categories = UnderCategory.objects.filter(category=category)
        context = {
            'under_categories': under_categories,
        }
        return render(request, 'product/category_detail.html', context)


class ProductsView(views.View):
    def get(self, request, pk, *args, **kwargs):
        under_category = get_object_or_404(UnderCategory, pk=pk)
        products = Product.objects.filter(under_category=under_category)
        context = {
            'products': products,
        }
        return render(request, 'catalog/products.html', context)


class ProductDetail(views.View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductAddToCartForm()
        context = {
            'product': product,
            'form': form
        }
        return render(request, 'catalog/product_detail.html', context)


class RegistrationCustomerView(views.View):
    """Регистрация для покупателя"""
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'registration/customer.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            messages.success(request,
                             'Вы успешно зарегестрированы!Рекомендуем отредактировать свой профиль,'
                             ' заказщики смотрят анкеты исполнителей')
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration/customer.html', context)


class LoginView(views.View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            context = {
                'form': form
            }
            return render(request, 'registration/login.html', context)


class LogoutUserView(LogoutView):
    next_page = 'base'
    template_name = 'base.html'


class ProductAddToCartView(views.View):
    def post(self, request, pk, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        form = ProductAddToCartForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     weight=cd['weight'],
                     update_weight=cd['update'])
        return HttpResponseRedirect('/cart/cart_detail/')


class CartDetailView(views.View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            item['update_weight_form'] = ProductAddToCartForm(
                initial={'weight': item['weight'],
                         'update': True})
        context = {
            'cart': cart,
        }
        return render(request, 'cart/cart_detail.html', context)


class ProductRemoveFromCartView(views.View):
    def post(self, product_id, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)

    def get(self, request, pk, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        cart.remove(product)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class OrderCreateView(views.View, Order):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm()
        context = {
            'cart': cart,
            'form': form,
        }
        return render(request, 'orders/order-create.html', context)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderProduct.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    weight=item['weight'],
                )
            cart.clear()
            new_order.delay(order.id)
            return render(request, 'orders/order-complete.html', {'order': order})


