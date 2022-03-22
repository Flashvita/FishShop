from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug}, args=[self.id])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class UnderCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField()
    description = models.TextField(max_length=300,  null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    under_category = models.ForeignKey(UnderCategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    image = models.ImageField(upload_to='catalogproducts/', null=True, blank=True, verbose_name='Изображение')
    price = models.DecimalField(max_digits=5, decimal_places=0,)
    manufacturer = models.CharField(max_length=100, null=True, blank=True, verbose_name='Производитель')
    weight = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True, verbose_name='Вес')
    available = models.BooleanField(default=True, verbose_name='Наличие товара')
    reviews = models.ForeignKey('Reviews', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Отзыв')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Reviews(models.Model):
    content = models.TextField(max_length=500, verbose_name='Отзыв')
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name='Покупатель')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_orders = models.ManyToManyField(Product, blank=True,
                                             verbose_name='Заказы покупателя',
                                             related_name='related_customer'
                                             )
    phone = models.CharField(max_length=11, verbose_name='номер телефона')
    address = models.TextField(null=True, blank=True, verbose_name='адресс')
    favourite = models.ManyToManyField(Product, verbose_name='Избранное')

    def __str__(self):
        return f"{self.user.name}"

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=11, verbose_name='телефон ')
    buying_type_choices = models.CharField(max_length=100, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES)
    address = models.CharField(max_length=200, verbose_name='Адресс', null=True, blank=True)















