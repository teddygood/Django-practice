# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

# CBV(Class Based View)
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template_name = 'blog/post_list.html'


class PostDetail(DetailView):
    model = Post

# FBV(Function Based View) Style
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )
