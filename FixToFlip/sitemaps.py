from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from FixToFlip.blog.models import BlogPost
from FixToFlip.blog.views import BlogPostView


class OfferSitemap(Sitemap):
    def items(self):
        return ['index', 'about-us', 'contact', 'faq', 'blog_main_page']

    def location(self, item):
        return reverse(item)



