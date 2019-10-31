from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse
from django.views.generic import DetailView ,ListView
from .models import Post, About # new

# Class Base View
class HomePage(ListView):
    model = Post
    template_name = 'home.html' 
    context_object_name = 'posts' 
    paginate_by = 6 # Adding Pagination

'''
# Function Base View
def HomePage(request):
    return render(request = request,
                  template_name='home.html',
                  context = {"posts":Post.objects.all})
'''

class BlogDetail(DetailView): # new 
    model = Post 
    template_name = 'post_detail.html'

class AboutPage(ListView): # new
    model = About
    template_name = 'about.html'

