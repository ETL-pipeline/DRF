# from rest_framework import serializers
# from blog.models import Blog

# class BlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blog
#         fields = '__all__'
from .models import Blog, Comment
from user.models import User
from rest_framework import serializers

class BlogCreateSerializer(serializers.ModelSerializer):
    writer          = serializers.ReadOnlyField(source='user.login_id')

    class Meta:
        model   = Blog
        fields  = ['title', 'writer', 'content'] 

class BlogListSerializer(serializers.ModelSerializer):
    writer          = serializers.ReadOnlyField(source='user.login_id')
    comments_count  = serializers.SerializerMethodField()

    class Meta:
        model   = Blog
        fields  = ['id', 'title', 'writer', 'created_at', 'view_count', 'comments_count']

    def get_comments_count(self, obj):
        comments = Comment.objects.filter(post_id=obj.id)
        comments_count = {
                'comments_count':len(comments)
                }
        return comments_count

class BlogDetailSerializer(serializers.ModelSerializer):
    writer      = serializers.ReadOnlyField(source='user.login_id')
    comments    = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = [{
                    'user'      :User.objects.get(id=comment.user_id).nickname,
                    'content'   :comment.content,
                    'created_at':comment.created_at,
                    'updated_at':comment.updated_at,
                } for comment in Comment.objects.filter(post_id=obj.id)]
        return comments

    class Meta:
        model   = Blog
        fields  = ['id', 'title', 'writer', 'content', 'view_count', 'updated_at', 'comments']

class CommentSerializer(serializers.ModelSerializer):
    writer       = serializers.ReadOnlyField(source='user.login_id')

    class Meta:
        model   = Comment
        fields  = ['id', 'writer', 'content', 'created_at', 'updated_at']