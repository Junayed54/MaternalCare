from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('api/login/', UserLoginView.as_view(), name="log_in"),
    
]


# Templates urls
urlpatterns += [
    path('login/', TemplateView.as_view(template_name='Html/html/sign-in-cover.html'), name='login'),
]
