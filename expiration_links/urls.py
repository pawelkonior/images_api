from django.urls import path

from expiration_links.views import ExpirationLinksView

expiration_link = ExpirationLinksView.as_view({'post': 'create'})
urlpatterns = [
    path('links/', expiration_link)
]
