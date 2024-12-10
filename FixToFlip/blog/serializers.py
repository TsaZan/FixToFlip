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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        image = (
            instance.image.url if instance.image else None
        )
        data['comment_count'] = instance.comments.count()
        post_data = {
            "id": data.get("id"),
            "title": data.get("title"),
            "slug": data.get("slug"),
            "image": image,
            "content": data.get("content"),
            "author": data.get("author"),
            "category": data.get("category"),
            "keywords": data.get("keywords"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
            "comment_count": data.get("comment_count"),
        }
        return post_data


class CategorySerializer(serializers.ModelSerializer):
    posts = BlogPostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id',
                  'name',
                  'posts',
                  ]
