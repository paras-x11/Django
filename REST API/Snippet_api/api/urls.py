from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path("registerUser/", registerUser, name="registerUser"),
    path("getUser/<int:id>/", getUser, name="getUser"),
    path("getUsers/", getUsers, name="getUsers"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("getSnippet/<int:id>/",getSnippet, name="getSnippet"),
    path("getSnippets/", getSnippets, name="getSnippets"),

    path("addSnippet/", addSnippet, name="addSnippet"),

    path("updateSnippet/<int:id>/", updateSnippet, name="updateSnippet"),
    path("deleteSnippet/<int:id>/", deleteSnippet, name="deleteSnippet"),

    path("getCommentsByUser/", getCommentsByUser, name="getCommentsByUser"),
    path("getCommentsBySnippet/<int:s_id>/", getCommentsBySnippet, name="getCommentsBySnippet"),

    path("postComment/<int:s_id>/", postComment, name="postComment"),

    path("updateComment/<int:c_id>/", updateComment, name="updateComment "),
    path("deleteComment/<int:c_id>/", deleteComment, name="deleteComment "),
]
