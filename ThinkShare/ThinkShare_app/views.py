from django.shortcuts import render,redirect,get_object_or_404
from .models import Article, ArticleImages,Vote,Comment,BookMark,Categories
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, ArticleForm,CommentForm,ContactForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator


def home(request):
    latest_articles = Article.objects.select_related('user').order_by('-created_at')[:3]
    trending_articles = (
        Article.objects.annotate(vote_count=Count('votes'))
        .order_by('-vote_count')[:4]
    )

    return render(request, 'home.html', {
        'latest_articles': latest_articles,
        'trending_articles': trending_articles,
    })

def articles(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    category_id = request.GET.get('category')
    author_name = request.GET.get('author_name', '').strip()

    articles = Article.objects.all().annotate(vote_count=Count('votes'))

    if category_id:
        articles = articles.filter(category_id=category_id)

    if author_name:
        articles = articles.filter(user__username__icontains=author_name)

    if sort_by == 'category':
        articles = articles.order_by('category__category_name')
    elif sort_by == 'vote':
        articles = articles.order_by('-vote_count')
    elif sort_by == 'author':
        articles = articles.order_by('user__username')
    else:  
        articles = articles.order_by('-created_at')

    if request.user.is_authenticated:
        for article in articles:
            article.is_bookmarked = article.bookmark_set.filter(user=request.user).exists()

    categories = Categories.objects.all()

    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'article/articles_view.html', {
        'articles': articles,
        'sort_by': sort_by,
        'categories': categories,
        'selected_category': category_id,
        'author_name': author_name,
        'articles': page_obj,
        'page_obj': page_obj,
    })

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
            return redirect('details', article.id)
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
            updated_article = form.save(commit=False)
            updated_article.user = request.user 
            updated_article.save()

            files = request.FILES.getlist('images')
            for f in files:
                ArticleImages.objects.create(article=updated_article, image_url=f)

            return redirect('details', updated_article.id)
    else:
        form = ArticleForm(instance=article)

    images = article.articleimages_set.all()
    return render(request, 'article/update_article.html', {'form': form, 'article': article,'images': images})

@login_required
def delete_article_image(request, article_id, pk):
    img = get_object_or_404(ArticleImages, id=pk, article__user=request.user)
    img.delete()
    return redirect('article_edit', pk=article_id)

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

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_profile':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')

        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if not check_password(old_password, user.password):
                messages.error(request, 'Your current password is incorrect.')
            elif new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password1) < 8:
                messages.error(request, 'New password must be at least 8 characters.')
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
                return redirect('profile')

    user_article = Article.objects.filter(user=user)
    user_comments = Comment.objects.filter(user=user)
    user_votes = Vote.objects.filter(user=user)

    return render(request, 'profile.html', {
        'user': user,
        'user_article': user_article,
        'user_comments': user_comments,
        'user_votes': user_votes,
    })


@login_required
def toggle_bookmark(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    bookmark, created = BookMark.objects.get_or_create(user=request.user, article=article)
    if not created:
        bookmark.delete()
    
    return redirect('articles')


def contact(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success = True  
            form = ContactForm() 
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form,'success': success})


@login_required
def bookmark_view(request):
    bookmarks = (
        BookMark.objects
        .filter(user=request.user)
        .select_related('article', 'article__category', 'article__user')
        .prefetch_related('article__articleimages_set')
    )
    paginator = Paginator(bookmarks, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_mark_list.html', {
        'bookmark': bookmarks,
        'articles': page_obj,
        'page_obj': page_obj,})


@login_required
def togglelist_bookmark(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    bookmark, created = BookMark.objects.get_or_create(user=request.user, article=article)
    if not created:
        bookmark.delete()

    return redirect('bookmark')
