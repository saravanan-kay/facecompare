from django.urls import path
from . import views

urlpatterns = [
    path('', views.compare_page, name='compare_page'),       # form/page
    path('api/compare/', views.api_compare, name='api_compare'),  # ajax/post endpoint
]
