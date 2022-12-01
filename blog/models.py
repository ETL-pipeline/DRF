from django.db import models
from user.models import User

class Blog(models.Model):
    # 1. 게시글의 id 값
    id = models.AutoField(primary_key=True, null=False, blank=False) 
    # 2. 제목
    title = models.CharField(max_length=100)
    # 3. 작성일
    created_at = models.DateTimeField(auto_now_add=True)
    # 4. 작성자
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # 5. 본문
    body = models.TextField()

class Comment(models.Model):
    id         = models.AutoField(primary_key=True, null=False, blank=False)
    user       = models.ForeignKey(
                'user.User',
                verbose_name = 'user',
                on_delete    = models.CASCADE
            )
    blog       = models.ForeignKey(
                'blog.Blog',
                verbose_name = 'blog',
                on_delete    = models.CASCADE
            )
    content    = models.CharField(
                verbose_name = 'content',
                max_length   = 128,
            )
    created_at = models.DateTimeField(
                verbose_name = 'created at',
                auto_now_add = True, 
            )
    updated_at = models.DateTimeField(
                verbose_name = 'updated at',
                auto_now     = True
            )
