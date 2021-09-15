from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

def photo_path(instance, filename):
    from time import strftime
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return '{}/{}/{}.{}'.format(strftime('post/%Y/%m/%d/'), instance.author.username, pid, extension)


# 게시글 모델 구현
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = ProcessedImageField(upload_to = photo_path,
                               processors=[ResizeToFill(600,600)],
                               format = 'JPEG',
                               options={'quality': 90})
    content = models.CharField(max_length=140, help_text="최대길이 140자 입력이 가능합니다")
    
    # many-to-many model 연결시키기
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          blank=True,
                                          related_name='like_user_set',
                                          through='Like') # post.like_set 으로 접근 가능
    
    bookmark_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                              blank=True,
                                              related_name='bookmark_user_set',
                                              through='Bookmark') # post.bookmark_set 으로 접근 가능
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        ordering = ['-created_at'] # 정렬: 최신순으로
        
    @property
    def like_count(self):
        return self.like_user_set.count()
    
    @property
    def bookmark_count(self):
        return self.bookmark_user_set.count()
    
        
    def __str__(self):
        return self.content

    
    
# 좋아요 모델 구현
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 좋아요를 누른 user인가?
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (
            ('user', 'post')
        )
        

        
# 북마크 모델 구현
class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 북마크를 누른 user인가?
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = (
            ('user', 'post')
        )
        
        

# 댓글 모델 구현
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # comment에 해당하는 post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # comment의 작성자
    content = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return self.content
    