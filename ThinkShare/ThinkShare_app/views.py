from django.shortcuts import render,redirect,get_object_or_404
from .models import Article, ArticleImages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ArticleForm,CommentForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
    articles = Article.objects.all()
    return render(request, 'home.html', {'articles': articles})

def about(request):
    return render(request, 'about.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can log in now.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()

            files = request.FILES.getlist('images')
            for f in files:
                ArticleImages.objects.create(article=article, image_url=f)

            return redirect('home')
    else:
        form = ArticleForm()

    return render(request, 'article/create_article.html', {'form': form})

def article_datails(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all().order_by('-created_at')

    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.save()
                return redirect('details', pk=article.pk)
        else:
            form = CommentForm()

    return render(request, 'article/details.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })
