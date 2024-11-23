from django.test import TestCase
from django.utils import timezone

from FixToFlip.accounts.models import BaseAccount
from FixToFlip.blog.models import Category, BlogPost


class BlogPostTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = BaseAccount.objects.create_user(username="testuser", password="password")
        cls.category = Category.objects.create(name="Test Category")

        for i in range(10):
            title = f"Test Post {i}"
            slug = f"test-post-{i}"
            BlogPost.objects.create(
                title=title,
                slug=slug,
                content="Test content",
                author=cls.user,
                category=cls.category
            )

    def create_blogpost_test(self):
        posts = BlogPost.objects.all()
        self.assertEqual(posts.count(), 10)

    def blogpost_slug_test(self):
        slugs = BlogPost.objects.values_list('slug', flat=True)
        self.assertEqual(len(slugs), len(set(slugs)))

    def blogpost_content_test(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(post.content, "Test content")

    def blogpost_author_test(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(post.author.username, "testuser")

    def blogpost_category_test(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(post.category.name, "Test Category")

    def blogpost_update_test(self):
        post = BlogPost.objects.get(slug="test-post-0")
        post.content = "Updated content"
        post.save()
        updated_post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(updated_post.content, "Updated content")

    def blogpost_delete_test(self):
        post = BlogPost.objects.get(slug="test-post-0")
        post.delete()
        with self.assertRaises(BlogPost.DoesNotExist):
            BlogPost.objects.get(slug="test-post-0")

    def blogpost_created_at_test(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertTrue(post.created_at <= timezone.now())

    def blogpost_filter_test(self):
        post = BlogPost.objects.get(slug="test-post-0")
        result = BlogPost.objects.filter(slug="test-post-0")
        self.assertIn(post, result)
