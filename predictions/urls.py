from django.urls import path
from .views import PredictView
from .views import index

urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('', index, name='index'),
]