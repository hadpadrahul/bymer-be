from rest_framework.routers import DefaultRouter

from catalog.views import MachineryViewSet, ProductCategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register("categories", ProductCategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("machinery", MachineryViewSet, basename="machinery")

urlpatterns = router.urls
