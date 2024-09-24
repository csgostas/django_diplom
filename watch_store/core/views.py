from django.shortcuts import render, HttpResponse, redirect
from .models import Article, Comment, User
from .forms import LoginForm, RegistrationForm, CommentForm, ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView, ListView, DeleteView
from core.models import models
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView


class home_view(ListView):
    model = Article
    template_name = 'core/index.html'
    context_object_name = 'articles'


def category_articles(request, category_id):
    articles = Article.objects.filter(category__id=category_id)
    context = {
        'articles': articles,
    }

    return render(request, 'core/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.article = article
            form.save()
            return redirect('article_detail', article.pk)
    else:
        form = CommentForm

    comments = Comment.objects.filter(article=article)
    context = {
        'article': article,
        'form': form,
        'comments': comments
    }
    return render(request, 'core/detail.html', context)


def favorite_list(request):
    return render(request, 'core/favorite_list.html')


def cart_detail(request):
    return render(request, 'core/cart_detail.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'core/login.html', context)


def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'core/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('article_detail', form.pk)

    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'core/article_form.html', context)


class UpdateArticleView(UpdateView):
    model = Article
    template_name = 'core/article_form.html'
    form_class = ArticleForm
    # success_url = '/'


class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'core/article_confirm_delete.html'
    success_url = '/'


class SearchResults(home_view):
    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = super().get_queryset()
        filtered = qs.filter(title__iregex=query)
        print(filtered)
        return filtered


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Article, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} - {self.product}'


class AboutProjectView(TemplateView):
    template_name = 'core/project.html'


class AboutAuthorView(TemplateView):
    template_name = 'core/author.html'


class CartView(TemplateView):
    template_name = 'core/cart_pay.html'
