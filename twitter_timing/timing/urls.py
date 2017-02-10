from django.conf.urls import url

from .views import get_best_posting_time

urlpatterns = [
    url(r'^get_best_posting_time/', get_best_posting_time),
]
