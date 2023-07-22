from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .card_viewset import CardViewSet

router = DefaultRouter()
router.register(r'card', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('card/drf-auth/', include('rest_framework.urls')),
    path('card/<pk>/freeze/', CardViewSet.as_view({'post': 'freeze'})),
    path('card/<pk>/unfreeze/', CardViewSet.as_view({'post': 'unfreeze'})),
]
