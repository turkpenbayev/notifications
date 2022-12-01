from rest_framework import routers


from notifications.views import *

router = routers.SimpleRouter()
router.register('health', HealthViewSet, 'health')
router.register('constants', ConstantsViewSet, 'constants')
router.register('customers', CustomerViewSet, basename='customers')
router.register('mailings', MailingViewSet, basename='mailings')

urlpatterns = [
    *router.urls,
]
