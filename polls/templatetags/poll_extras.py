from django import template
from jalali_date import datetime2jalali, date2jalali

register = template.Library()


# @register.filter(name='cut')
# def cut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, "")
#
#
# register.filter("cut", cut)
@register.filter(name='show_date')
def show_date(value):
    return date2jalali(value)


@register.filter(name='show_time')
def show_date(value):
    return datetime2jalali(value)


@register.filter(name='there_digits_number')
def there_digits_number(value: int):
    return ' {:,} تومان'.format(value)


@register.simple_tag(name='multiply')
def multiply(num, price, *args, **kwargs):
    return there_digits_number(num * price)
