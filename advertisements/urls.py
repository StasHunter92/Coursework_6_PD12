from django.urls import path

from advertisements import views

# ----------------------------------------------------------------------------------------------------------------------
# Create advertisement and comment urls
urlpatterns = [
    path('ads/', views.AdvertisementsViewSet.as_view({'get': 'list', 'post': 'create'}), name='ad-list'),
    path('ads/<int:pk>/', views.AdvertisementsViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='ad-detail'),
    path('ads/<int:ad_id>/comments/', views.CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comment-list'),
    path('ads/<int:ad_id>/comments/<int:pk>/', views.CommentViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='comment-detail'),
    path('ads/me/', views.AdvertisementUserListView.as_view(), name='user-ads'),
]
