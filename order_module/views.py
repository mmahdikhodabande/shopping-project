from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import json
from django.template.loader import render_to_string
from django.urls import reverse

from order_module.models import Order, Order_details
from product_module.models import Product


def Cart_orders(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_amount = 0
    for detail_order in current_order.order_details_set.all():
        total_amount += detail_order.product.price * detail_order.count
    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'order_module/Cart_order.html', context)


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({'status': 'not_found',
                             'text': 'تعداد مورد نظر یافت نشد '})
    product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
    if request.user.is_authenticated:
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.order_details_set.filter(product_id=product.id).first()
            if current_order_detail is not None:
                current_order_detail.count += int(count)
                current_order_detail.save()
            else:
                new_detail = Order_details(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()
            return JsonResponse({'status': 'success',
                                 'text': 'به سبد خرید اضافه شد !'})
    else:
        return JsonResponse({'status': 'not_authent',
                             'text': 'لطفا توگام نخست وارد سایت شوید '})


def delete_order_in_basket(request: HttpRequest):
    detail_id = request.GET.get('detail_id')

    if detail_id is None:
        return JsonResponse({'status': 'NotFound_detail_id'})

    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    detail = current_order.order_details_set.filter(pk=detail_id).first()
    if detail is None:
        return JsonResponse({
            'status': 'not_found_detail'
        })
    detail.delete()
    total_amount = 0
    for detail_order in current_order.order_details_set.all():
        total_amount += detail_order.product.price * detail_order.count
    context = {
        'order': current_order,
        'sum': total_amount
    }
    data = render_to_string('order_module/Cart_order_component.html', context)
    return JsonResponse({'status': 'success',
                         'body': data
                         })


def change_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    num_order = request.GET.get('num_order')
    if detail_id is None or num_order is None:
        return JsonResponse({'status': 'NotFound_detail_id_or_num_order'})

    order_detail = Order_details.objects.filter(pk=detail_id, order__user_id=request.user.id,
                                                order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({'status': 'Not_found_order_detail'})

    if num_order == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif num_order == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({'status': 'num_order_invalid'})

    current_order, created = Order.objects.prefetch_related('order_details_set').get_or_create(is_paid=False,
                                                                                               user_id=request.user.id)
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount,
    }
    data = render_to_string('order_module/Cart_order_component.html', context)
    return JsonResponse({'status': 'success',
                         'body': data
                         })


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "اینجا باید پول ودی "  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/order/verify/'


@login_required
def send_request(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('Cart_order'))
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


@login_required
def verify(authority, request):
    current_order, created = Order.objects.get_or_create(is_paid=False,
                                                         user_id=request.user.id)  # اینجا امکان داره ارور بده چون از request استفاده نشد حواست جمع کن
    total_price = current_order.calculate_total_price()
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
