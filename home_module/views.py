from django.db.models import Count, Sum
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from account_module.models import User
from home_module.forms import Add_email_off_ModelForm
from home_module.models import add_email_for_off
from site_module.models import ads_baner
from django.views.generic.base import TemplateView
from product_module.models import Product, ProductCategory
from utils.convertors import slider_list
from site_module.models import SiteSetting, FooterLinkBox, Slider


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        context['baner_ADS'] = ads_baner.objects.filter(is_active=True,
                                                        position__iexact=ads_baner.baner_position.home_page)
        latest_post = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:5]
        context['slider_list'] = slider_list(latest_post, 4)
        categories = list(ProductCategory.objects.annotate(
            products_count=Count('product_categories')).filter(is_active=True,
                                                               is_delete=False,
                                                               products_count__gt=0)[:6])
        category_products = []
        for i in categories:
            item = {
                'id': i.id,
                'title': i.title,
                'products': list(i.product_categories.all()[:4])

            }
            category_products.append(item)
        context['category_products'] = category_products

        Best_selling_products = Product.objects.filter(order_details__order__is_paid=True).annotate(order_count=Sum(
            'order_details__count'
        )).order_by('-order_count')
        context['Best_selling_products'] = slider_list(Best_selling_products, 3)

        product_visit = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('product_visit')).order_by('-visit_count')[:12]
        context['product_visited'] = slider_list(product_visit, 4)
        return context


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    current_user = User.objects.filter(id=request.user.id).first()
    for item in footer_link_boxes:
        item.footerlink_set
    if request.method == 'POST':
        email_form = Add_email_off_ModelForm(request.POST)
        if email_form.is_valid():
            email_user = email_form.cleaned_data.get('email')
            user: bool = User.objects.filter(email__iexact=email_user).exists()
            if user:
                email_form.add_error('email', 'ایمیل وارد شده تکراری می باشد')
            else:
                new_email = add_email_for_off(
                    email=email_user
                )
                new_email.save()
                return redirect(reverse('user_panel'))

    email_form = Add_email_off_ModelForm()

    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes,
        'form': email_form,
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context


# def send_email(request: HttpRequest):
#     if request.method == 'POST':
#         email_form = Add_email_off_ModelForm(request.POST)
#         if email_form.is_valid():
#             print(email_form.cleaned_data)
#             return redirect('user_panel')
#
#     email_form = Add_email_off_ModelForm()
#     context = {
#         'form': email_form,
#     }
#     return render(request, 'home_module/news_email.html', context)
