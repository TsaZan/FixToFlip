from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve
from django.conf.urls.static import static

from FixToFlip import settings
from FixToFlip.sitemaps import OfferSitemap

sitemaps = {"static": OfferSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("FixToFlip.api_urls"), name="url_api"),
    path("accounts/", include("allauth.urls"), name="account"),
    path("account/", include("FixToFlip.accounts.urls"), name="account_main_page"),
    path("blog/", include("FixToFlip.blog.urls"), name="blog_main_page"),
    path("credits/", include("FixToFlip.credits.urls"), name="credits_main_page"),
    path("offers/", include("FixToFlip.offers.urls"), name="offers_main_page"),
    path(
        "properties/", include("FixToFlip.properties.urls"), name="properties_main_page"
    ),
    path("", include("FixToFlip.common.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"properties": OfferSitemap}},
        name="django.contrib.sitemaps",
    ),
    path("dashboard/", include("FixToFlip.dashboard.urls"), name="dashboard_main_page"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
