from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AccountViews, ActivationMail

urlpatterns = [
    url('account/',AccountViews.as_view()),
    url('mail/',ActivationMail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)