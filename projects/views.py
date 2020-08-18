from django.shortcuts import render, redirect
from .models import Post, Comment
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets, permissions
from .serializers import PostSerializer, CommentSerializer

# Create your views here.
def index(request):
    title = 'Home'
    all_posts = Post.get_all_posts()
   
    context = {
        'posts': all_posts,
    }
    return render(request, 'welcome.html', context)

class PostDetailView(DetailView):
    model = Post

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = ['title','url','tech_used','desc', 'image_url']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','url','desc', 'image_url']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

@login_required
def add_comment(request, post_id):
    post = Post.objects.filter(pk=post_id)
    all_posts = Post.get_all_posts()   
    context = {
        'posts': all_posts,
    }
    if request.method == 'POST':
        content = request.POST.get('comment')
        comment_inst = Comment(content=content, post_id=post_id)      
        comment_inst.save()  
        return redirect('welcome')
        
    return render(request, 'index.html', context)
        

@login_required
def add_like(request, post_id):
    post = Post.objects.filter(pk=post_id).first()
    post.likes += 1
    post.save()
    all_posts = Post.get_all_posts()   
    context = {
        'posts': all_posts,
    }    
        
    return render(request, 'index.html', context)

@login_required
def search_user(request):
    if 'user' in  request.GET and request.GET['user']:
        search_psn = request.GET.get("user")
        found_user = User.objects.filter(username=search_psn).first()
        print(found_user.id)
        posts = Post.objects.filter(user=found_user.id)

        context = {
            'user': found_user,
            'posts': posts
        }
        
        return render(request, 'spec_user.html', context)
    return redirect('welcome')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer