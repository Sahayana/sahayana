
from datetime import time
from django.shortcuts import render,get_object_or_404,redirect,resolve_url
from .models import *
from .forms import *
from django.utils import timezone
from django.core.paginator import Paginator # Paginator 호출
from django.contrib.auth.decorators import login_required # login 데코레이터
from django.contrib import messages
from django.db.models import Q, Count, F
# Create your views here.

def post_list(request, main_category_slug=None, category_slug = None):
    # Category filtering
    current_category = None  
    categories = Category.objects.all()
    posts = Post.objects.filter(display=True)

    if main_category_slug and category_slug:
        main_category = get_object_or_404(MainCategory, slug = main_category_slug)
        current_category = get_object_or_404(Category, main_category = main_category, slug = category_slug)
        posts = posts.filter(category = current_category)
    

    # 페이징/ 검색/ 정렬 파라미터
    page = request.GET.get('page', '1') 
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    # Search
    if kw:
        posts = posts.filter(
            Q(title__icontains=kw)|
            Q(content__icontains=kw)|
            Q(comment__content__icontains=kw)        
        )

    # Sorting
    if so == 'recommend':
        posts = posts.annotate(num_recommend = Count('recommend')).order_by('-num_recommend', '-created_date')    
    elif so == 'popular':
        posts = posts.annotate(num_comment = Count('comments')).order_by('-num_comment', '-created_date')
    else:   # 'recent'
        posts = posts.order_by('-created_date')    
    
    
    # Paginator    
    paginator = Paginator(posts, '9')
    page_obj = paginator.get_page(page)
    

    context = {'categories':categories, 'current_category':current_category, 'posts':page_obj, 'page':page, 'kw':kw, 'so':so}

    return render(request, 'blog/post_list.html', context=context)

def post_detail(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    context = {'post':post}
    
    return render(request, 'blog/post_detail.html', context=context)


def post_create(request, category_slug = None):
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug = category_slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data            
            post = Post(title = cd['title'], content = cd['content'], category = current_category)
            post.save()
            return redirect('blog:post_detail', post.id)
    else:
        form = PostForm()
    context = {'form':form}
    
    return render(request, 'blog/post_form.html', context)

def post_update(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', id=post.id)
    
    else:
        form = PostForm(instance=post)

    context = {'form':form}
    
    return render(request, 'blog/post_form.html', context)


def post_delete(request, post_id):
        
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('blog:post_all')


#---------------------- Comment ------------------------#

@login_required
def comment_create(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('blog:post_detail', post.id), comment.id))   
    else:
        form = CommentForm()
    context = {'post':post,'form':form}
    return render(request, 'blog/post_detail.html', context)


@login_required
def comment_update(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.updated_date = timezone.now()
            comment.save()
            return  redirect('{}#comment_{}'.format(resolve_url('blog:post_detail', comment.post.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form':form}
    return render(request, 'blog/comment_form.html', context)


@login_required
def comment_delete(request, comment_id):
    
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return  redirect('blog:post_detail', post_id=comment.post.id)

#---------------------- Recommend ------------------------#

@login_required
def post_recommend(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    user = request.user
    
    if user.is_superuser:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        post.recommend.add(request.user)
    return redirect('blog:post_detail', post.id)

@login_required
def comment_recommend(request, comment_id):
    
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author:
        messages.error(request, '본인이 작성한 댓글은 추천할 수 없습니다.')
    else:
        comment.recommend.add(request.user)
    return redirect('{}#comment_{}'.format(resolve_url('blog:post_detail', comment.post.id), comment.id))

 