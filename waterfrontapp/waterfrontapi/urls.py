from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, basename='login')
router.register('leads', views.ContactFormViewSet)
router.register('posts', views.PostViewSet)
# router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
# router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    # path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls))
]