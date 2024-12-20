from cloudinary.models import CloudinaryField
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from FixToFlip.validators import bad_words_validator


class BlogPost(models.Model):
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("blog_post_page", args=[str(self.slug)])

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(10, "Title must be at least 10 characters long"),
        ],
    )

    slug = models.SlugField(unique=True, editable=False, null=False, max_length=150)

    keywords = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Keywords that describe the post, separated by commas",
    )

    image = CloudinaryField(
        "image",
        blank=True,
        null=True,
    )

    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    category = models.ForeignKey(
        "blog.Category",
        on_delete=models.CASCADE,
        related_name="posts",
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            if not self.pk:
                super().save(*args, **kwargs)
            self.slug = slugify(f"{self.pk}-{self.title}", allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def comment_count(self):
        return self.comments.count()


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(
        max_length=30,
        unique=True,
    )

    @property
    def post_count(self):
        return self.posts.count()

    def __str__(self):
        return self.name


class Comment(models.Model):
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField(
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(10, "Comment must be at least 10 characters long"),
            bad_words_validator,
        ],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
