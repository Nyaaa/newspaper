from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, SearchResults

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', SearchResults.as_view(), name='search'),
]
