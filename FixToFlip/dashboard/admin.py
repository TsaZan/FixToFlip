from django.contrib import admin
from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from cities_light.admin import SubRegion, City, Country, Region
from django.contrib.sites.models import Site
from djmoney.contrib.exchange.admin import Rate
from allauth.socialaccount.admin import SocialAccountAdmin, SocialTokenAdmin, SocialAppAdmin

admin.site.unregister(Country)
admin.site.unregister(City)
admin.site.unregister(Region)
admin.site.unregister(SubRegion)
admin.site.unregister(Rate)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)



