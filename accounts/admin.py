from django.contrib import admin
from .models import Profile


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'user']
    list_display_links = ['nickname', 'user'] # 클릭할 수 있는 링크
    search_fields = ['nickname'] # 검색창