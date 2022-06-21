from profile_api import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('view_set', views.HelloViewSet, basename='view_set')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)


urlpatterns=[
   path('hello/', views.HellowApiView.as_view()),
   path("login/", views.UserLoginApiView.as_view()),
   path('', include(router.urls))
]