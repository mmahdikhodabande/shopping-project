from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.http import Http404, HttpRequest

from home_module.models import add_email_for_off
from order_module.models import Order
from .forms import edit_panel_User_ModelForm, change_pass_ModelForm
from account_module.models import User
from django.contrib.auth import logout
from django.urls import reverse


# Create your views here.
@method_decorator(login_required, name="dispatch")
class main_user_panelView(TemplateView):
    template_name = 'user_panel/user_panel.html'


@login_required(login_url='login_page')
def template_user_panel_components(request: HttpRequest):
    return render(request, 'user_panel/components/user_panel_component.html')


@method_decorator(login_required, name="dispatch")
class edit_panel_user(View):
    def get(self, request: HttpRequest):
        curent_user = User.objects.filter(id=request.user.id).first()
        edite_Form = edit_panel_User_ModelForm(instance=curent_user)
        context = {
            'edite_Form': edite_Form,
            'curent_user': curent_user
        }
        return render(request, 'user_panel/edit_panel_user.html', context)

    def post(self, request: HttpRequest):
        curent_user = User.objects.filter(id=request.user.id).first()
        edite_Form = edit_panel_User_ModelForm(request.POST, request.FILES, instance=curent_user)
        if edite_Form.is_valid():
            edite_Form.save(commit=True)
        context = {
            'edite_Form': edite_Form
        }
        return render(request, 'user_panel/edit_panel_user.html', context)


@method_decorator(login_required, name="dispatch")
class change_pass(View):
    def get(self, request: HttpRequest):
        context = {
            'form_pass': change_pass_ModelForm()
        }

        return render(request, 'user_panel/change_pass.html', context)

    def post(self, request: HttpRequest):
        form_pass = change_pass_ModelForm(request.POST)
        if form_pass.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form_pass.cleaned_data.get('current_pass')):
                current_user.set_password(form_pass.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form_pass.add_error('current_pass', 'رمز عبور اشتباه است ')
        context = {
            'form_pass': form_pass
        }

        return render(request, 'user_panel/change_pass.html', context)


class show_list_shopping(ListView):
    model = Order
    template_name = 'user_panel/show_list_shopping.html'

    def get_queryset(self):
        query = super(show_list_shopping, self).get_queryset()
        query = query.filter(user_id=self.request.user.id, is_paid=True)
        return query


def show_detail_shopping(request, detail_id):
    order = Order.objects.prefetch_related('order_details_set').filter(pk=detail_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('محصولی یافت نشد .')

    return render(request, 'user_panel/detail_shopping.html', {'order': order})
