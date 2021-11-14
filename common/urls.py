from django.urls import include, path
from rest_framework.routers import SimpleRouter
from common.views import error500API

app_name = 'common'

router = SimpleRouter()
router.register('common', error500API, basename='common')

urlpatterns = [
    path('', include(router.urls)),
]
