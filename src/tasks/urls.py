from rest_framework import routers


from tasks.views import *

router = routers.SimpleRouter()
router.register('health', HealthViewSet, 'health')
router.register('auth', AuthViewSet, 'auth')
router.register('todo', ToDoViewSet, basename='todo')

urlpatterns = [
    *router.urls,
]
