from django.contrib.sitemaps import Sitemap
from django.urls import reverse



class OfferSitemap(Sitemap):
    def items(self):
        return ['index',
                'about-us',
                'contact',
                'faq',
                'blog_main_page'
                ]

    def location(self, item):
        return reverse(item)



