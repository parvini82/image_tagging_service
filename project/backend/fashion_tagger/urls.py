from django.urls import path

from .views import ImageTagView

urlpatterns = [
    path("tag/", ImageTagView.as_view(), name="image-tag"),
]
