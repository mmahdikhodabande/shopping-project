from django.db import models

# Create your models here.
from account_module.models import User
from product_module.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=' مشتری ')
    is_paid = models.BooleanField(verbose_name='نهایی شذه /نهایی نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.order_details_set.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            for order_detail in self.order_details_set.all():
                total_amount += order_detail.product.price * order_detail.count

        return total_amount

    def __str__(self):
        return str(self.user)


    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class Order_details(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سفارش مشتری')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price =models.IntegerField(null=True, blank=True,verbose_name='قیمت نهایی برای پرداخت')
    count = models.IntegerField(verbose_name='تعداد سفارش محصول ')

    def __str__(self):
        return str(self.order.user)
    class Meta:
        verbose_name = 'جزییات سفارش'
        verbose_name_plural = 'جزییات سفارشات'
