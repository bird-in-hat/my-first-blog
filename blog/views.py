from django.shortcuts import render

# Create your views here.

from django.utils.timezone import now
from .models import Post
from django.core.exceptions import ObjectDoesNotExist
from .forms import PostForm
from django.shortcuts import redirect


def post_list(request):
    posts = Post.objects.filter(publish_date__lte=now()).order_by('publish_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, 'blog/error.html', {'text': 'Error: Post not found'})

    return render(request, 'blog/post_detail.html', {'post': post})

def post_edit(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, 'blog/error.html', {'text': 'Error: Post not found'})

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_new.html', {'form': form})

def post_new(request):
    if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.publish()
                return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_new.html', {'form': form})

def not_found(request):
    return render(request, 'blog/error.html', {'text': 'Error: Page not found'})
