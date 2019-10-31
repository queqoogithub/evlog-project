from django.urls import path 
from .views import HomePage, BlogDetail, AboutPage

urlpatterns = [ 
    #path('', HomePage, name='home'), # กรณีใช้ Function Base View
    path('', HomePage.as_view(), name='home'), 
    path('post/<int:pk>/', BlogDetail.as_view(), name='post_detail'), # new 
    path('about/', AboutPage.as_view(), name='about'), # new
] 
