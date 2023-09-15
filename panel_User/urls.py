from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_user_panelView.as_view(), name='user_panel'),
    path('edit_user_panel', views.edit_panel_user.as_view(), name='edit_user_panel'),
    path('change_pass', views.change_pass.as_view(), name='change_pass'),
    path('component', views.template_user_panel_components, name='component_panel'),
    path('show_list_shop', views.show_list_shopping.as_view(), name='show_list_shop'),
    path('show_list_shop/<detail_id>/', views.show_detail_shopping, name='show_detail_shop'),

]
