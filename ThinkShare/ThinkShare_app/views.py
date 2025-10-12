from django.shortcuts import render,redirect,get_object_or_404
from .models import Article, ArticleImages,Vote,Comment
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ArticleForm,CommentForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse


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

def article_details(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all().order_by('-created_at')

    form = CommentForm() if request.user.is_authenticated else None

    user_liked = article.liked_by(request.user) if request.user.is_authenticated else False
    user_disliked = article.disliked_by(request.user) if request.user.is_authenticated else False

    if request.user.is_authenticated and request.method == "POST":
        if 'comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.save()
                return redirect('details', pk=article.pk)
        elif 'vote' in request.POST:
            value = int(request.POST.get('vote'))
            existing_vote = Vote.objects.filter(article=article, user=request.user).first()

            if existing_vote:
                if existing_vote.value == value:
                    existing_vote.delete()
                else:
                    existing_vote.value = value
                    existing_vote.save()
            else:
                Vote.objects.create(article=article, user=request.user, value=value)
            return redirect('details', pk=article.pk)

    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'user_liked': user_liked,
        'user_disliked': user_disliked,
    }
    return render(request, 'article/details.html', context)


@login_required
def update_article(request, pk):
    article = get_object_or_404(Article, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('details', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article/update_article.html', {'form': form, 'article': article})


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk, user=request.user)
    delete_url = reverse('article_delete', args=[article.pk])  
    
    if request.method == 'POST':
        article.delete()
        return redirect('home')

    return render(request, 'article/confirm_delete.html', {
        'object_type': 'article',
        'object_content': article.title,
        'delete_url': delete_url,
        'cancel_url': reverse('details', args=[article.pk])
    })


@login_required
def update_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('details', pk=comment.article.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'article/update_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    article_id = comment.article.pk

    if request.method == "POST":
        comment.delete()
        return redirect('details', pk=article_id)
    
    cancel_url = reverse('details', args=[article_id]) if comment.article else '/'

    return render(request, 'article/confirm_delete.html', {
        'object_type': 'comment',
        'object_content': comment.content,
        'cancel_url': cancel_url
    })

@login_required
def profile_view(request):
    user = request.user
    user_comments = Comment.objects.filter(user=user).order_by('-created_at')
    user_votes = Vote.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'profile.html', {
        'user': user,
        'user_comments': user_comments,
        'user_votes': user_votes
    })

