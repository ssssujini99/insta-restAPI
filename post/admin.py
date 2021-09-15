from django.contrib import admin
from .models import Post, Like, Bookmark, Comment
from django import forms

# Register your models here.

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Post
        fields = '__all__'
        
        
class LikeInline(admin.TabularInline):
    model = Like
    
class CommentInline(admin.TabularInline):
    model = Comment

        
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'nickname', 'content', 'created_at']
    list_display_links = ['author', 'nickname', 'content']
    form = PostForm
    inlines = [LikeInline, CommentInline]
    
    def nickname(request, post):
        return post.author.profile.nickname # nickname이 post에 들어있지 않으니까 / 외래키에 있는 값 가져오기
    

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_display_links = ['post', 'user']
    
    
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'created_at']
    list_display_links = ['post', 'user']
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'content', 'author', 'created_at']
    list_display_links = ['post', 'content', 'author']





