from django.urls import path
from . import views

urlpatterns = [
    path('', views.Article_list_View.as_view(), name='article_list'),
    path('cat/<str:category>', views.Article_list_View.as_view(), name='articles_by_category'),
    path('<pk>', views.detail_article_View.as_view(), name='detail_article'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
]
