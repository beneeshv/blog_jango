from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Post, Category, Comment, UserProfile, Rating
from .forms import PostForm, CommentForm, UserProfileForm, UserRegistrationForm
from django.utils.text import slugify

def post_list(request):
    posts = Post.objects.filter(status='published')
    search_query = request.GET.get('q')
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'search_query': search_query,
        'categories': Category.objects.all()
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(parent=None)
    user_rating = 0
    
    if request.user.is_authenticated:
        try:
            user_rating = post.ratings.get(user=request.user).value
        except Rating.DoesNotExist:
            pass
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('blog:post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'categories': Category.objects.all(),
        'user_rating': user_rating
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('blog:post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status='published')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'blog/category_detail.html', {
        'category': category,
        'posts': posts
    })

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if post.is_disliked_by(request.user):
            post.dislikes.remove(request.user)
        if post.is_liked_by(request.user):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return JsonResponse({
            'success': True,
            'likes': post.get_likes_count(),
            'dislikes': post.get_dislikes_count(),
            'is_liked': post.is_liked_by(request.user),
            'is_disliked': post.is_disliked_by(request.user)
        })
    return JsonResponse({'success': False}, status=400)

@login_required
def dislike_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if post.is_liked_by(request.user):
            post.likes.remove(request.user)
        if post.is_disliked_by(request.user):
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
        return JsonResponse({
            'success': True,
            'likes': post.get_likes_count(),
            'dislikes': post.get_dislikes_count(),
            'is_liked': post.is_liked_by(request.user),
            'is_disliked': post.is_disliked_by(request.user)
        })
    return JsonResponse({'success': False}, status=400)

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'blog/profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("blog:post_list")  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "registration/login.html")

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Redirect to the login page after logout

@login_required
def rate_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        value = int(request.POST.get('value', 0))
        if 1 <= value <= 5:
            rating, created = Rating.objects.update_or_create(
                post=post,
                user=request.user,
                defaults={'value': value}
            )
            messages.success(request, 'Your rating has been submitted successfully!')
            return redirect('blog:post_detail', slug=slug)
        else:
            messages.error(request, 'Please select a valid rating.')
    
    return render(request, 'blog/rate_post.html', {'post': post})

