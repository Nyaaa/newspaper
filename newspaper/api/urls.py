from django.urls import re_path, path

from .views import NewsViewSet, ArticleViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'news', NewsViewSet)
router.register(r'articles', ArticleViewSet)
urlpatterns = router.urls

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Newspaper API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
]
