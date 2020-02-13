from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import BlogPostForm

def index(request):
    """The home page for Blog."""
    return render(request, 'blogs/index.html')
    
def posts(request):
    """Show all posts"""
    posts = BlogPost.objects.order_by('date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)
"""
def post(request, post_id):
    Show single post and its text
    post = BlogPost.objects.get(id=post_id)
    context = {'post': post}
    return render(request, 'blogs/post.html', context)
"""
@login_required
def new_post(request):
    """Add a new post."""    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BlogPostForm
    else:
        # POST data submitted; process data.
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:posts')
            
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def edit_post(request, post_id):
    """Edit posts."""
    post = BlogPost.objects.get(id=post_id)
    check_post_owner(request, post.owner)
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:posts')
            
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def check_post_owner(request, owner):
    """Check post owner."""
    if owner != request.user:
        raise Http404
