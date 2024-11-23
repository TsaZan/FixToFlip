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

    def test_create_blogpost(self):
        posts = BlogPost.objects.all()
        self.assertEqual(posts.count(), 10)

    def test_blogpost_slug(self):
        slugs = BlogPost.objects.values_list('slug', flat=True)
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_blogpost_content_(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(post.content, "Test content")

    def test_blogpost_author(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(post.author.username, "testuser")

    def test_blogpost_category(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(post.category.name, "Test Category")

    def test_blogpost_update(self):
        post = BlogPost.objects.get(slug="test-post-0")
        post.content = "Updated content"
        post.save()
        updated_post = BlogPost.objects.get(slug="test-post-0")
        self.assertEqual(updated_post.content, "Updated content")

    def test_blogpost_delete(self):
        post = BlogPost.objects.get(slug="test-post-0")
        post.delete()
        with self.assertRaises(BlogPost.DoesNotExist):
            BlogPost.objects.get(slug="test-post-0")

    def test_blogpost_created_at(self):
        post = BlogPost.objects.get(slug="test-post-0")
        self.assertTrue(post.created_at <= timezone.now())

    def test_blogpost_filter(self):
        post = BlogPost.objects.get(slug="test-post-0")
        result = BlogPost.objects.filter(slug="test-post-0")
        self.assertIn(post, result)
