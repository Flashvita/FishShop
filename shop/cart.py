from .models import Product
from decimal import Decimal
from django.conf import settings


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, weight=1, update_weight=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'weight': 0, 'price': str(product.price)}
        if update_weight:
            self.cart[product_id]['weight'] = int(weight)
        else:
            self.cart[product_id]['weight'] += int(weight)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, *args, **kwargs):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['weight']
            yield item

    def __len__(self):
        return sum(item['weight'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['weight']
            for item in self.cart.values()
                )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
