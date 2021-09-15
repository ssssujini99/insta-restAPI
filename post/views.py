from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.http import HttpResponse
from .models import Post, Like, Comment
from .forms import PostForm


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
    
    
@login_required
@require_POST
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)
    
    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"
        
    context = {'like_count': post.like_count,
              'message': message}
    
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@require_POST
def post_bookmark(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_bookmark, post_bookmark_created = post.bookmark_set.get_or_create(user=request.user)
    
    if not post_bookmark_created:
        post_bookmark.delete()
        message = "북마크 취소"
    else:
        message = "북마크"
    
    context = {'bookmark_count': post.bookmark_count,
              'message': message}
    
    return HttpResponse(json.dumps(context), content_type="application/json")
        
        

@login_required #로그인이 되어있어야만 실행됨
def post_new(request):
    if request.method == 'POST':
        PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # 중복방지
            post.author = request.user
            post.save()
            #post.tag_save()
            messages.info(request, '새 글이 등록되었습니다')
            return redirect('post:post_list')
    else:
        form = PostForm()
        return render(request, 'post/post_new.html', {'form': form})
    

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, '잘못된 접근입니다')
        return redirect('post:post_list')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            #post.tag_set.clear()
            #post.tag_save()
            #messages.success(request, '수정완료')
            return redirect('post:post_list')
    else: # get방식일때
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {
        'post': post,
        'form': form,
    })
            
            
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user or request.method == 'GET':
        #messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')
    
    if request.method == 'POST':
        post.delete()
        #messages.success(request, '삭제완료')
        return redirect('post:post_list')
    
    


@login_required
def comment_new(request): # ajax로 댓글을 추가할 때 처리하기
    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk) # pk로 댓글에 대한 Post 찾기
    if request.method == 'POST': # ajax에서 전달한 요청이 post일때
        form = CommentForm(request.POST) # 사용자가 작성한 댓글폼을 post로 가져옴
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return render(request, 'post/comment_new_ajax.html', {
                'comment': comment,
            })
    return redirect("post:post_list")


@login_required
def comment_delete(request): # ajax로 댓글에 대한 삭제 요청이 들어왔을 때 처리하기
    pk = request.POST.get('pk')
    comment = get_object_or_404(Comment, pk=pk) # 해당 삭제할 댓글을 가져오기
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        message = '삭제완료'
        status = 1
    else:
        message = '잘못된 접근입니다'
        status = 0
    
    return HttpResponse(json.dumps({'message': message, 'status': status, }), content_type="application/json")


        
    







