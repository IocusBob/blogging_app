from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm, CommentForm
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from blog.models import Comments, Post

# Standard template view/generating basic html using a template
class AboutView(TemplateView):
    template_name = 'about.html'

# standard List View of Posts WITH an SQL query in the form of python code
class PostListView(ListView):
    model = Post

    # The below is a Field Lookup, check book notes for more info
    def get_queryset(self):
        #                                          lte = less than or equal to
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # Basically, the above results to SQL: SELECT * FROM Post WHERE
    # published_date <= NOW() ORDER BY published_date DESC

# Detail view of a single post, a pk is required here which we get from the
# urls.py file.
class PostDetailView(DetailView):
    model=Post

# The LoginRequiredMixin allows us to 'mix in' another class that allows a
# login check automatically without any effort
class CreatePostView(LoginRequiredMixin, CreateView):
    # If the person isnt logged in, we will redirect them to /login/ BUT we can
    # leave this out and by default the user will be redirected to settings.login_url (if there is one)
    login_url='/login/'
    # If the user is successful with logging in then we redirect to the following:
    redirect_field_name = '/blog/post_detail.html'
    # The below imports the forms from blog.forms.py to be rendered when this
    # view is called. Thus it knows what fields to include and what css attributes
    # to assign etc.
    form_class=PostForm
    # This links above form and THIS view to the Post model
    model=Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url='/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class=PostForm
    model=Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model=Post
    # If post is deleted, redirect to the post_list url.
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model=Post
    template_name = 'blog/post_draft_list.html'


    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

@login_required
def post_publish(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

# ++++++++++++COMMENTS VIEWS++++++++++++++

@login_required
def add_comments_to_post(request, pk):
    # The get_object_or_404 will pass in the primary key and try to access the
    # specific record assigned to that pk from the Post class. This is stored
    # in the post variable.
    post = get_object_or_404(Post, pk=pk)
    if request.method== 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # We dont want to commit save yet...
            comment=form.save(commit=False)
            # ...because we need to also give the post(Foreignkey) to the newly
            # created comment below
            comment.post = post
            # and then we save
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment=get_object_or_404(Comments, pk=pk)
    # Here we have grabbed the comment and have simply called its own approve()
    # method on it.
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    # Because we are deleting the comment we will lost the pk THUS we store it
    # here in a variable so that when it is deleted, we retain the pk
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
