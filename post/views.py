from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def post_list(request):
    
    post_list = Post.objects.all()
    
    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)
        # 여기까지는 장고 내장모델 model 을 찾는 과정
        user_profile = user.profile
        # 정의해둔 모델 profile에서 해당 데이터 찾기
        
        return render(request, 'post/post_list.html', {
            'user_profile': user_profile,
            'posts': post_list,
        })
    else:
        return render(request, 'post/post_list.html', {
            'posts': post_list,
        })
        