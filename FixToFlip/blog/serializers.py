from rest_framework import serializers

from FixToFlip.blog.models import BlogPost, Category


class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y")
    updated_at = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = BlogPost
        fields = ['title',
                  'slug',
                  'keywords',
                  'image',
                  'content',
                  'author',
                  'category',
                  'created_at',
                  'updated_at',
                  ]


class CategorySerializer(serializers.ModelSerializer):
    posts = BlogPostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  'posts',
                  ]
