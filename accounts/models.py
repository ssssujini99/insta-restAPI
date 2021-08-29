from django.conf import settings
from django.db import models
from imagekit.models import ProcessedImageField #이미지 처리
from imagekit.processors import ResizeToFill

def user_path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range()]
    pid = ''.join(arr)
    extension = filename.split('.')[-1] # 확장자 부분 가져오기
    return 'accouts/{}/{}.{}'.format(instance.user.username, pid, extension)


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField('별명', max_length=20, unique=True) # unique=True: 중복허용x
    picture = ProcessedImageField(upload_to=user_path,
                                  processors=[ResizeToFill(150, 150)], # 이미지 사진 조절
                                  format='JPEG',
                                  options={'quality': 90},
                                  blank=True,
                                 )
    about = models.CharField(max_length=300, blank=True) # 자기소개 부분
    GENDER_C = ( # gender select 하기
        ('선택안함', '선택안함'),
        ('여성', '여성'),
        ('남성', '남성'),
    )
    gender = models.CharField('성별(선택사항)',
                             max_length=10,
                             choices=GENDER_C,
                             default='N')
    
    def __str___(self):
        return self.nickname # nickname을 대표로 함