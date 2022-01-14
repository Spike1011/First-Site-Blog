import random

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import News, Category, Inspection
from .forms import NewsForm
from .utils import MyMixin


class HomeNews(MyMixin, ListView):
    # название модели со списком
    model = News
    # название нужного html
    template_name = 'news/home_news_list.html'
    # название в html
    context_object_name = 'news'
    # если нуно передать в шаблон переменные, лучше только статические
    # extra_context = {'title': 'Главная'}

    paginate_by = 2

    # метод вызывается когда выполняется запрос данных из класса
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        context['data'] = [1, 4, 5, 6]
        return context

    # используется для фильтрации списка или изменения его
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 2
    # запрет на показ пустых списков, если откроем категорию которой нету или же нету записей в категории
    # allow_empty = False

    # метод вызывается когда выполняется запрос данных из класса
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk = self.kwargs['category_id']))

        context['data1'] = [i + 1 * self.kwargs['category_id'] for i in [18, 4, 15, 6, 67]]
        context['data2'] = [i + 2 * self.kwargs['category_id'] for i in [11, 14, 15, 16, 6]]
        context['data3'] = [i + 3 * self.kwargs['category_id'] for i in [1, 4, 5, 6, 7]]
        context['labels'] = [str(i) for i in range(5)]
        return context

    # используется для филтрации списка или изменения его
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    # template_name = 'news/news_detail.html'
    # pk_url_kwarg = 'news_id'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')
    # login_url = '/admin/'     # кидает на ввод логина и пароль в админ
    # raise_exception = True    # возбуждаем ошибку если не авторизован пользотель


def get_category(request, category_id):
    news = News.objects.filter(category_id = category_id)
    category = Category.objects.get(pk=category_id)

    context = {
        'news': news,
        'title': 'Список новостей',
        'category': category,
    }
    return render(request, 'news/category.html', context=context)


def test_index(request):
    return render(request, 'news/test.html')


def test_dashboard_index(request, coef):
    grid_table = Inspection.objects.all().order_by('pk')
    values = Inspection.objects.all().values('created_at')

    list =[]

    for i in values:
        list.append(i['created_at'])

    context = {
        'grid_table': grid_table,
        #'dataChart': [i + 1 * coef for i in [15, 41, 52, 6, 5, 1]],
        #'dataChart': [random.random() for i in range(200)],
        'dataChart': [i['value'] for i in Inspection.objects.all().values('value').order_by('pk')],
        #'labels': [i + 1 * coef for i in range(20000)],
        #'labels': [str(i) for i in range(20)],
        'labels': [i['title'] for i in Inspection.objects.all().values('title').order_by('pk')],
        'coef': coef
    }
    #print(coef)
    print(context['dataChart'])
    return render(request, 'news/test_dashboard.html', context=context)



'''
def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
    }

    return render(request, 'news/index.html', context=context)
'''

'''
def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})
'''

'''
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # news = News.objects.create(**form.cleaned_data)
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()

    return render(request, 'news/add_news.html', {'form': form})
'''