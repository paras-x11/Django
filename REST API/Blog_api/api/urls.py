from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView)
from django.urls import path
from api.views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', UserAPI.as_view(), name='users'),

    path('blogs/', BlogAPI.as_view(), name='blogs'),
    path('blogs/user/', UserBlogsAPI.as_view(), name='blogsByUser'),
    path('blogs/<int:id>/', ModifyBlogAPI.as_view(), name='modifyBlogs'),

    path('blogs/comments/<int:b_id>/', CommentAPI.as_view(), name='comments'),
    path('comments/user/', UserCommentsAPI.as_view(), name='commmentsByUSer'),
    path('comments/<int:c_id>/', ModifyCommentAPI.as_view(), name='modifyComment'),

    path('blogs/likes/<int:b_id>/', LikeAPI.as_view(), name='likes'),
    path('likes/user/', UserLikesAPI.as_view(), name='LikesByUser'),

]
