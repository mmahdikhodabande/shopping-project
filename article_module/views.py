from .models import Article, ArticleCategory, Article_comment
from django.views.generic.list import ListView
from django.views import View
from django.views.generic.detail import DetailView
from jalali_date import datetime2jalali, date2jalali
from django.http import Http404, HttpRequest,HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView,FormView
from .forms import Article_commentModelForm
# Create your views here.

# class ArticleViw(View):
#     def get(self, request):
#         article_list = Article.objects.filter(is_active=True)
#         context = {'list_article': article_list}
#         return render(request, 'article_module/article_list.html', context)
#
#     def get_context_data(self, *args,  **kwargs):
#         context = super(Article_list_View, self).get_context_data(*args,**kwargs)
#         context['date']=datetime2jalali(self.request.user.date_joined)
#         return context

class Article_list_View(ListView):
    model = Article
    paginate_by = 1
    template_name = 'article_module/article_list.html'

    def get_queryset(self):
        query = super(Article_list_View, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query

    def get_context_data(self, *args, **kwargs):
        context = super(Article_list_View, self).get_context_data(*args, **kwargs)
        # context['date'] = date2jalali(self.request.user.date_joined)
        return context


def article_categories_partial(request: HttpRequest):
    article_first = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,
                                                                                           parent_id=None)
    context = {
        'first_article': article_first
    }
    return render(request, 'article_module/components/article_category_component.html', context)


class detail_article_View(DetailView):
    model = Article
    template_name = 'article_module/article_detail.html'
    paginate_by = 1


    def get_queryset(self):
        find_query = super(detail_article_View, self).get_queryset()
        find_query = find_query.filter(is_active=True)
        return find_query

    def get_context_data(self, **kwargs):
        context = super(detail_article_View, self).get_context_data()
        article: Article_comment = kwargs.get('object')
        context['comments'] = Article_comment.objects.filter(article_id=article.id, parent=None).order_by('-creat_date').prefetch_related(
            'article_comment_set')
        return context


def submit_comment(request :HttpRequest):
    if request.user.is_authenticated:
        article_comment=request.GET.get('article_comment')
        article_id=request.GET.get('article_id')
        parent_id=request.GET.get('parent_Id')
        print(parent_id,article_comment,article_id)
        new_comment :ArticleComment =Article_comment(article_id=article_id, parent_id=parent_id ,text=article_comment,user_id=request.user.id)
        new_comment.save()
    return HttpResponse('Response')