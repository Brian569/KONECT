from django.urls import path
from Social.views import (
    PostList, SinglePost, ProfileView,
    LandingView, AddPost, EditProfile, 
    PostEdit, PostDelete, DeleteComment,
    Addfollower, RemoveFollower, AddLike,
    Dislike, UserSearch
    )

urlpatterns = [
    path('', LandingView.as_view(), name='home'),
    path('addpost', AddPost.as_view(), name='addpost'),
    path('posts', PostList.as_view(), name='post_list'),
    path('single_post/<int:pk>', SinglePost.as_view(), name='single_post'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile_edit/<int:pk>', EditProfile.as_view(), name='profile_edit'),
    path('post_edit/<int:pk>', PostEdit.as_view(), name='post_edit'),
    path('post_delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
    path('comment_delete/<int:pk>', DeleteComment.as_view(), name='comment_delete'),
    path('add_followers/<int:pk>', Addfollower.as_view(), name='add_followers'),
    path('remove_followers/<int:pk>', RemoveFollower.as_view(), name='remove_followers'),
    path('post/<int:pk>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', Dislike.as_view(), name='dislike'),
    path('search/', UserSearch.as_view(), name='profile_search')

]