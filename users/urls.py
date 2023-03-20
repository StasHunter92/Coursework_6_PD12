from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import MyUserViewSet

# ----------------------------------------------------------------------------------------------------------------------
# Create router
users_router = SimpleRouter()
users_router.register(r'users', MyUserViewSet)

# ----------------------------------------------------------------------------------------------------------------------
# Create user and token urls
urlpatterns = [
    path('', include(users_router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
