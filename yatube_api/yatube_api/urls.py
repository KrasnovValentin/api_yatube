from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from api.views import PostViewSet, GroupViewSet, CommentViewSet

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet, basename='posts')
v1_router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                   basename='comments')
v1_router.register('groups', GroupViewSet, basename='groups')
urlpatterns = [
    path('api/v1/', include(v1_router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
