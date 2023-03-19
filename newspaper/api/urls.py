from .views import NewsViewSet, ArticleViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'news', NewsViewSet)
router.register(r'articles', ArticleViewSet)
urlpatterns = router.urls
